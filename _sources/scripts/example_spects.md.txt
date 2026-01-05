---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
import pathlib

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pyprojroot

import crowsetta
```

```{code-cell} ipython3
def plot_spect(S_db, sr, ylim=None, 
               hop_length=512, win_length=512, x_coords=None,
               figsize=(10, 4), dpi=300, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

    img = librosa.display.specshow(S_db, sr=sr, hop_length=hop_length, win_length=win_length, 
                                   x_coords=x_coords, y_axis='linear', x_axis='time', ax=ax)

    if ylim:
        ax.set_ylim(ylim)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
```

```{code-cell} ipython3
def plot_labels(labels,
                t,
                t_shift_label=0.01,
                y=0.4,
                ax=None,
                text_kwargs=None):
    """plot labels on an axis.

    Parameters
    ----------
    labels : list, numpy.ndarray
    t : numpy.ndarray
        times (in seconds) at which to plot labels
    t_shift_label : float
        amount (in seconds) that labels should be shifted to the left, for centering.
        Necessary because width of text box isn't known until rendering.
    y : float, int
        height on y-axis at which segments should be plotted.
        Default is 0.5.
    ax : matplotlib.axes.Axes
        axes on which to plot segment. Default is None,
        in which case a new Axes instance is created
    text_kwargs : dict
        keyword arguments passed to the `Axes.text` method
        that plots the labels. Default is None.

    Returns
    -------
    text_list : list
        of text objections, the matplotlib.Text instances for each label
    """
    if text_kwargs is None:
        text_kwargs = {}

    if ax is None:
        fig, ax = plt.subplots

    text_list = []    
    
    for label, t_lbl in zip(labels, t):
        t_lbl -= t_shift_label
        text = ax.text(t_lbl, y, label, **text_kwargs, label='label')
        text_list.append(text)
    
    return text_list
```

```{code-cell} ipython3
def plot_segments(
    annot,
    label_color_map,
    ax,
    tlim=None,
    y_segments=0.4,
    h_segments=0.4,
    y_labels=0.3,
    text_kwargs=None
):
    rectangles = []

    labels = []
    onsets = []
    offsets = []
    for seg in annot.seq.segments:
        label, onset_s, offset_s = seg.label, seg.onset_s, seg.offset_s
        if tlim:
            if offset_s < tlim[0] or onset_s > tlim[1]:
                continue
        labels.append(label)
        onsets.append(onset_s)
        offsets.append(offset_s)
    
    labels = np.array(labels)
    onsets = np.array(onsets)
    offsets = np.array(offsets)
    
    for label, onset_s, offset_s in zip(labels, onsets, offsets):
        rectangle = plt.Rectangle(
            (onset_s, y_segments), 
            width=offset_s - onset_s,
            height=h_segments,
            facecolor=label_color_map[label]
        )
        ax.add_patch(rectangle)
        rectangles.append(rectangle)
    
    t = onsets + ((offsets - onsets) / 2)
    plot_labels(labels, t=t, y=y_labels, text_kwargs=text_kwargs, ax=ax)

    if tlim:
        ax.set_xlim(tlim)

    return rectangles
```

```{code-cell} ipython3
def make_fig(audio_path, annot_path, fig_path, tlim=None):
    tg = crowsetta.formats.by_name('simple-seq').from_file(annot_path)
    annot = tg.to_annot()

    labelset = set(
        [segment.label for segment in annot.seq.segments]
    )

    cmap = plt.cm.get_cmap('tab20')
    colors = [cmap(ind) for ind in range(len(labelset))]
    label_color_map = {label: color for label, color in zip(labelset, colors)}

    y, sr = librosa.load(audio_path, sr=None)  # sr=None to keep original sampling rate
    # y = y[tlim_inds_snippet[0]:tlim_inds_snippet[1]]
    
    hop_length=256
    win_length=512

    D = librosa.stft(y, hop_length=hop_length, win_length=win_length)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    idx = np.array(range(0, S_db.shape[1]))
    x_coords = librosa.frames_to_time(idx, sr=sr, hop_length=hop_length, n_fft=2048)
    # x_coords = x_coords + TLIM_S_ORIGINAL[0]

    FONT_SIZE = 14

    plt.rc('font', size=FONT_SIZE)
    plt.rc('axes', labelsize=FONT_SIZE)
    plt.rc('xtick', labelsize=FONT_SIZE)
    plt.rc('ytick', labelsize=FONT_SIZE)

    fig = plt.figure(constrained_layout=True, figsize=(10, 6), dpi=300)
    gs = fig.add_gridspec(5, 1)
    ax_arr = []
    ax_arr.append(
        fig.add_subplot(gs[:3,:])
    )
    ax_arr.append(
        fig.add_subplot(gs[3:,:])
    )

    ax_arr = np.array(ax_arr)

    plot_spect(S_db, sr, 
               hop_length=hop_length, win_length=win_length, 
               x_coords=x_coords,
               ylim=[128, 11000], ax=ax_arr[0])
    if tlim:
        ax_arr[0].set_xlim(tlim)

    _ = plot_segments(annot=annot, label_color_map=label_color_map, 
                      text_kwargs={'fontsize': FONT_SIZE}, ax=ax_arr[1], tlim=tlim)

    ax_arr[1].set(xticks=[], yticks=[])
    ax_arr[1].set_frame_on(False)

    plt.savefig(fig_path, bbox_inches='tight')
```

```{code-cell} ipython3
# DATASET_ROOT = pyprojroot.here() / 'data/bfsongrepo'
DATASET_ROOT = pathlib.Path('/media/pimienta/Backup/vocal/BFSongRepo/')

EXAMPLE_AUDIO_ANNOT_BY_BIRD_ID = {
    'bl26lb16': {
        'audio': '041912/bl26lb16_190412_0721.20144.wav',
        'annot': '041912/bl26lb16_190412_0721.20144.cbin.csv',
        'tlim': [22.4, 23.8],
    },
    'gr41rd51': {
        'audio': '061912/gr41rd51__3part_SYLc_th4191_belowhits_190612_0710.239.wav',
        'annot': '061912/gr41rd51__3part_SYLc_th4191_belowhits_190612_0710.239.cbin.csv',
        'tlim': [3, 5.2],
    },
    'gy6or6': {
        'audio': '032212/gy6or6_baseline_220312_0836.3.wav',
        'annot': '032212/gy6or6_baseline_220312_0836.3.cbin.csv',
        'tlim': [4.25, 5.9],
    },
    'or60yw70': {
        'audio': '092712/or60yw70_270912_0729.1196.wav',
        'annot': '092712/or60yw70_270912_0729.1196.cbin.csv',
        'tlim': [2.3, 6.35],
    },
}

IMAGES_ROOT = pyprojroot.here() / 'docs/images'
```

```{code-cell} ipython3
for bird_id, data_d in EXAMPLE_AUDIO_ANNOT_BY_BIRD_ID.items():
    audio_path, annot_path = data_d['audio'], data_d['annot']
    tlim = data_d['tlim']
    audio_path = DATASET_ROOT / bird_id / audio_path
    annot_path = DATASET_ROOT / bird_id / annot_path
    fig_path = IMAGES_ROOT / f'{bird_id}_key.png'
    make_fig(audio_path, annot_path, fig_path, tlim=tlim)
```

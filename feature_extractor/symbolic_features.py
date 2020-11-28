from music21 import converter, corpus, instrument, midi, note, chord, pitch, environment
from music21.midi import translate
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
environment.set('musicxmlPath', '/usr/bin/musescore3')
#environment.set('graphicsPath', '/usr/bin/lodraw')
environment.set('lilypondPath', '/home/zappatistas20/bin/lilypond')


def open_midi(midi_path, remove_drums):
    # There is an one-line method to read MIDIs
    # but to remove the drums we need to manipulate some
    # low level MIDI events.
    mf = midi.MidiFile()
    mf.open(midi_path)
    mf.read()
    mf.close()
    if remove_drums:
        for i in range(len(mf.tracks)):
            mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10]

    return translate.midiFileToStream(mf)


def list_instruments(midi):
    part_stream = midi.parts.stream()
    print("List of instruments found on MIDI file:")
    for p in part_stream:
        aux = p
        print(p.partName)


def extract_notes(midi_part):
    parent_element = []
    ret = []
    for nt in midi_part.flat.notes:
        if isinstance(nt, note.Note):
            ret.append(max(0.0, nt.pitch.ps))
            parent_element.append(nt)
        elif isinstance(nt, chord.Chord):
            for pitch in nt.pitches:
                ret.append(max(0.0, pitch.ps))
                parent_element.append(nt)

    return ret, parent_element


def print_parts_countour(midi):
    fig = plt.figure(figsize=(12, 5))
    ax = fig.add_subplot(1, 1, 1)
    minPitch = pitch.Pitch('C10').ps
    maxPitch = 0
    xMax = 0

    # Drawing notes.
    for i in range(len(midi.parts)):
        top = midi.parts[i].flat.notes
        y, parent_element = extract_notes(top)
        if (len(y) < 1): continue

        x = [n.offset for n in parent_element]
        ax.scatter(x, y, alpha=0.6, s=7)

        aux = min(y)
        if (aux < minPitch): minPitch = aux

        aux = max(y)
        if (aux > maxPitch): maxPitch = aux

        aux = max(x)
        if (aux > xMax): xMax = aux

    for i in range(1, 10):
        linePitch = pitch.Pitch('C{0}'.format(i)).ps
        if (linePitch > minPitch and linePitch < maxPitch):
            ax.add_line(mlines.Line2D([0, xMax], [linePitch, linePitch], color='red', alpha=0.1))

    plt.ylabel("Note index (each octave has 12 notes)")
    plt.xlabel("Number of quarter notes (beats)")
    plt.title('Voices motion approximation, each color is a different instrument, red lines show each octave')
    plt.show()


if __name__ == '__main__':
    base_midi = open_midi('../temp/test_dataset/0a2d626401e49eb46c59ec6dbd4f048fa305b001.mid', True)
    base_midi.show()
    list_instruments(base_midi)
    print_parts_countour(base_midi.measures(0, 6))
    base_midi.plot('histogram', 'pitchClass', 'count')
    base_midi.plot('scatter', 'offset', 'pitchClass')
    timeSignature = base_midi.getTimeSignatures()[0]
    music_analysis = base_midi.analyze('key')
    print("Music time signature: {0}/{1}".format(timeSignature.beatCount, timeSignature.denominator))
    print("Expected music key: {0}".format(music_analysis))
    print("Music key confidence: {0}".format(music_analysis.correlationCoefficient))
    print("Other music key alternatives:")
    for analysis in music_analysis.alternateInterpretations:
        if analysis.correlationCoefficient > 0.5:
            print(analysis)

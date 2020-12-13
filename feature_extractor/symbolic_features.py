from music21 import *
from music21.midi import translate
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from config.paths import musescore_path, lilypond_path
from mido import MidiFile
import mido

environment.set('musicxmlPath', musescore_path)
# environment.set('graphicsPath', '/usr/bin/lodraw')
environment.set('lilypondPath', lilypond_path)

KEEP_FEATS = ['AverageMelodicIntervalFeature', 'MostCommonMelodicIntervalFeature',
              'DistanceBetweenMostCommonMelodicIntervalsFeature', 'MostCommonMelodicIntervalPrevalenceFeature',
              'RelativeStrengthOfMostCommonIntervalsFeature', 'NumberOfCommonMelodicIntervalsFeature',
              'AmountOfArpeggiationFeature', 'RepeatedNotesFeature', 'ChromaticMotionFeature', 'StepwiseMotionFeature',
              'MelodicThirdsFeature', 'MelodicFifthsFeature', 'MelodicTritonesFeature', 'MelodicOctavesFeature',
              'DirectionOfMotionFeature', 'DurationOfMelodicArcsFeature', 'SizeOfMelodicArcsFeature',
              'MostCommonPitchPrevalenceFeature', 'MostCommonPitchClassPrevalenceFeature',
              'RelativeStrengthOfTopPitchesFeature', 'RelativeStrengthOfTopPitchClassesFeature',
              'IntervalBetweenStrongestPitchesFeature', 'IntervalBetweenStrongestPitchClassesFeature',
              'NumberOfCommonPitchesFeature', 'PitchVarietyFeature', 'PitchClassVarietyFeature', 'RangeFeature',
              'MostCommonPitchFeature', 'PrimaryRegisterFeature', 'ImportanceOfBassRegisterFeature',
              'ImportanceOfMiddleRegisterFeature', 'ImportanceOfHighRegisterFeature', 'MostCommonPitchClassFeature',
              'NoteDensityFeature', 'AverageNoteDurationFeature', 'VariabilityOfNoteDurationFeature',
              'MaximumNoteDurationFeature', 'MinimumNoteDurationFeature', 'StaccatoIncidenceFeature',
              'AverageTimeBetweenAttacksFeature', 'VariabilityOfTimeBetweenAttacksFeature',
              'AverageTimeBetweenAttacksForEachVoiceFeature',
              'AverageVariabilityOfTimeBetweenAttacksForEachVoiceFeature', 'InitialTempoFeature',
              'InitialTimeSignatureFeature', 'CompoundOrSimpleMeterFeature', 'TripleMeterFeature',
              'QuintupleMeterFeature', 'ChangesOfMeterFeature', 'DurationFeature',
              'MaximumNumberOfIndependentVoicesFeature', 'AverageNumberOfIndependentVoicesFeature',
              'VariabilityOfNumberOfIndependentVoicesFeature', 'QualityFeature', 'TonalCertainty',
              'UniqueNoteQuarterLengths', 'MostCommonNoteQuarterLength', 'MostCommonNoteQuarterLengthPrevalence',
              'RangeOfNoteQuarterLengths', 'UniquePitchClassSetSimultaneities', 'UniqueSetClassSimultaneities',
              'MostCommonPitchClassSetSimultaneityPrevalence', 'MostCommonSetClassSimultaneityPrevalence',
              'MajorTriadSimultaneityPrevalence', 'MinorTriadSimultaneityPrevalence',
              'DominantSeventhSimultaneityPrevalence', 'DiminishedTriadSimultaneityPrevalence',
              'TriadSimultaneityPrevalence', 'DiminishedSeventhSimultaneityPrevalence',
              'IncorrectlySpelledTriadPrevalence', 'ComposerPopularity', 'LandiniCadence', 'LanguageFeature']


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


def note_count(measure, count_dict):
    bass_note = None
    for chord in measure.recurse().getElementsByClass('Chord'):
        # All notes have the same length of its chord parent.
        note_length = chord.quarterLength
        for note in chord.pitches:
            # If note is "C5", note.name is "C". We use "C5"
            # style to be able to detect more precise inversions.
            note_name = str(note)
            if (bass_note is None or bass_note.ps > note.ps):
                bass_note = note

            if note_name in count_dict:
                count_dict[note_name] += note_length
            else:
                count_dict[note_name] = note_length

    return bass_note


def simplify_roman_name(roman_numeral):
    # Chords can get nasty names as "bII#86#6#5",
    # in this method we try to simplify names, even if it ends in
    # a different chord to reduce the chord vocabulary and display
    # chord function clearer.
    ret = roman_numeral.romanNumeral
    inversion_name = None
    inversion = roman_numeral.inversion()

    # Checking valid inversions.
    if ((roman_numeral.isTriad() and inversion < 3) or
            (inversion < 4 and
             (roman_numeral.seventh is not None or roman_numeral.isSeventh()))):
        inversion_name = roman_numeral.inversionName()

    if (inversion_name is not None):
        ret = ret + str(inversion_name)

    elif (roman_numeral.isDominantSeventh()):
        ret = ret + "M7"
    elif (roman_numeral.isDiminishedSeventh()):
        ret = ret + "o7"
    return ret


def harmonic_reduction(midi_file):
    ret = []
    temp_midi = stream.Score()
    temp_midi_chords = midi_file.chordify()
    temp_midi.insert(0, temp_midi_chords)
    music_key = temp_midi.analyze('key')
    max_notes_per_chord = 4
    for m in temp_midi_chords.measures(0, None):  # None = get all measures.
        if (type(m) != stream.Measure):
            continue

        # Here we count all notes length in each measure,
        # get the most frequent ones and try to create a chord with them.
        count_dict = dict()
        bass_note = note_count(m, count_dict)
        if (len(count_dict) < 1):
            ret.append("-")  # Empty measure
            continue

        sorted_items = sorted(count_dict.items(), key=lambda x: x[1])
        sorted_notes = [item[0] for item in sorted_items[-max_notes_per_chord:]]
        measure_chord = chord.Chord(sorted_notes)

        # Convert the chord to the functional roman representation
        # to make its information independent of the music key.
        roman_numeral = roman.romanNumeralFromChord(measure_chord, music_key)
        ret.append(simplify_roman_name(roman_numeral))

    return ret


class SymbolicFeatureExtractor(object):
    def __init__(self, quarter_length_divisors=(4, 3), get_names=True):
        """
        :param quarter_length_divisors: tuple. (2,) will snap all events to eighth note grid.
                                        (4, 3) will snap events to sixteenth notes and eighth note triplets,
                                        whichever is closer. (4, 6) will snap events to sixteenth notes and
                                        sixteenth note triplets. If quarterLengthDivisors is not specified
                                        then the default is (4, 3).
        """
        self.quarter_length_divisors = quarter_length_divisors
        self.parsed_stream = None
        self.available_extractors = self.get_available_extractors()
        self.instruments = []
        self.duration_in_secs = None
        self.file_path = None
        self.multi_value_feats = []
        self.get_names = get_names

    @staticmethod
    def get_available_extractors():
        available_extractors = {}
        ex_id = 0
        fs = features.jSymbolic.extractorsById
        for k in fs:
            for i in range(len(fs[k])):
                if fs[k][i] is not None:
                    if fs[k][i] in features.jSymbolic.featureExtractors:
                        n = fs[k][i].__name__
                        if n != 'QualityFeature' and n in KEEP_FEATS:
                            available_extractors[ex_id] = {'type': k, 'ID': i, 'name': n, 'method': 'jSymbolic'}
                            ex_id += 1

        fsn = features.native.featureExtractors
        for ext in fsn:
            n = ext.__name__
            if n in KEEP_FEATS:
                available_extractors[ex_id] = {'name': n, 'method': 'native'}
                ex_id += 1
        return available_extractors

    def print_formatted_feats(self):
        for key, value in self.available_extractors.items():
            print("\\hline \n {} & {} & {} & {} \\\\".format(key+1, value['method'], value['name'], ""))

    def get_feature_names(self):
        names = []
        for v in self.available_extractors.values():
            names.append(v['name'])
        return names

    def remove_drums(self):
        keep_inst = []
        for i, inst in enumerate(self.instruments):
            try:
                name = str(inst.name)
                lower_inst = name.lower()
                if lower_inst.find('drums') < 0 and lower_inst.find('percussion') < 0:
                    keep_inst.append(i)
            except AttributeError:
                keep_inst.append(i)
        return keep_inst

    def preprocess_with_mido(self):
        mid = MidiFile(filename=self.file_path, clip=True)
        self.instruments = mid.tracks
        self.duration_in_secs = mid.length

    def parse_midi(self, midi_path, remove_drums=True):
        # There is an one-line method to read MIDIs
        # but to remove the drums we need to manipulate some
        # low level MIDI events.
        self.file_path = midi_path
        try:
            self.preprocess_with_mido()
        except EOFError:
            remove_drums = False
        if remove_drums:
            keep_instruments = self.remove_drums()
        mf = midi.MidiFile()
        mf.open(self.file_path)
        mf.read()
        mf.close()
        if remove_drums:
            for i in range(len(mf.tracks)):
                mf.tracks[i].events = [ev for ev in mf.tracks[i].events if i in keep_instruments]
        stream = translate.midiFileToStream(mf)

        self.parsed_stream = stream.quantize(self.quarter_length_divisors)

    def apply_extractor_jsymbolic(self, extractor):
        fe = getattr(features.jSymbolic, extractor)(self.parsed_stream)
        try:
            f = fe.extract()
            if extractor == 'InitialTimeSignatureFeature':
                try:
                    return [f.vector[0] / f.vector[1]]
                except ZeroDivisionError:
                    return 'null'
            else:
                return f.vector
        except TypeError:
            print('error extracting {}'.format(extractor))
            return 'null'
        except features.jSymbolic.JSymbolicFeatureException:
            print('error extracting {}'.format(extractor))
            return 'null'

    def apply_extractor_native(self, extractor):
        fe = getattr(features.native, extractor)(self.parsed_stream)
        try:
            f = fe.extract()
            return f.vector
        except TypeError:
            print('error extracting {}'.format(extractor))
            return 'null'
        except features.native.NativeFeatureException:
            print('error extracting {}'.format(extractor))
            return 'null'

    def extract_symbolic_features(self, midi_path, accept_multivalues=False):
        self.parse_midi(midi_path)
        feats = {}
        for extractor_method in self.available_extractors.values():
            if extractor_method['method'] == 'jSymbolic':
                v = self.apply_extractor_jsymbolic(extractor_method['name'])
            else:
                v = self.apply_extractor_native(extractor_method['name'])
            try:
                if accept_multivalues or len(v) == 1:
                    feats[extractor_method['name']] = v[0]
                else:
                    feats[extractor_method['name']] = 'null'
            except TypeError:
                feats[extractor_method['name']] = 'null'
        # feats['PlaybackDuration'] = self.duration_in_secs
        if self.get_names:
            return list(feats.values()), list(feats.keys())
        else:
            return list(feats.values())

    def melodic_interval_histogram(self):
        fe = features.jSymbolic.MelodicIntervalHistogramFeature(self.parsed_stream)
        f = fe.extract()
        return f.vector

    def most_common_interval(self):
        fe = features.jSymbolic.MostCommonMelodicIntervalFeature(self.parsed_stream)
        f = fe.extract()
        return f.vector

    def most_common_pitch(self):
        fe = features.jSymbolic.MostCommonPitchClassFeature(self.parsed_stream)
        f = fe.extract()
        return f.vector

    def minimum_note_duration(self):
        fe = features.jSymbolic.MinimumNoteDurationFeature(self.parsed_stream)
        f = fe.extract()
        return f.vector

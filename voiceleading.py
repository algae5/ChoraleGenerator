"""
An implementation of voice leading via python.

David Berghoff
"""

import itertools
import random

PITCH_MAPPING = {"C": 0, "B#": 0, "Dbb": 0, "B##": 1, "C#": 1, "Db": 1,
"C##": 2, "D": 2, "Ebb": 2, "D#": 3, "Eb": 3, "Fbb": 3, "D##": 4, "E": 4, "Fb": 4,
"E#": 5, "F": 5, "Gbb": 5, "E##": 6, "F#": 6, "Gb": 6, "F##": 7, "G": 7, "Abb": 7,
"G#": 8, "Ab": 8, "G##": 9, "A": 9, "Bbb": 9, "A#": 10, "Bb": 10, "Cbb": 10,
"A##": 11, "B": 11, "Cb": 11}

SCALE_NOTES = "ABCDEFGABCDEFGABCDEFGABCDEFGABCDEFG"

REGISTER_MAX = 9
REGISTER_MIN = 0

def _check_valid_note(note_name):
	"""
	Checks that the given note is a valid note in the given harmonic system.
	"""
	if note_name not in PITCH_MAPPING:
		raise TypeError, str(note_name) + " is not a valid note name"

def _check_valid_octave(octave):
	"""
	Checks that the given octave is valid within the given register.
	"""
	if (type(octave) != int) or (octave < REGISTER_MIN) or (octave > REGISTER_MAX):
		raise TypeError, str(octave) + " is not a valid octave"

class Note:
	"""
	A note in traditional diatonic harmonic systems.
	Notated using sicentific pitch notation, where middle C is C4, and A (440Hz)
	is A4, or the first A above C4, and the octave is a number from 0 to 9.
	Note names are given as strings, such as "C" or "Cb" or "C#".
	B flat below middle C, for example, is "Bb" (octave 3).
	Furthermore, a number is assigned to each note name, where C is 0, C# is 1, etc.
	"""
	def __init__(self, note_name, octave):
		_check_valid_note(note_name)
		_check_valid_octave(octave)

		self._octave = octave
		self._note_name = note_name
		self._note_number = PITCH_MAPPING[note_name]

	def __str__(self):
		string = ""
		if len(self._note_name) == 1:
			return string + self._note_name + str(self._octave)
		if len(self._note_name) == 3:
			if self._note_name[2] == "b":
				return string + self._note_name[0] + "-double-flat " + str(self._octave)
			else:
				return string + self._note_name[0] + "-double-sharp " + str(self._octave)
		if self._note_name[1] == "b":
			return string + self._note_name[0] + "-flat " + str(self._octave)
		else:
			return string + self._note_name[0] + "-sharp " + str(self._octave)

	def __eq__(self, other_note):
		"""
		Returns True if the two notes are identical in octave, pitch, and name.
		Thus, E-flat does not equal D-sharp.
		"""
		# If the notes are in different octaves, they are not equal.
		if self._octave != other_note.get_octave():
			return False

		# Because strings cannot be compared directly.
		other_note_name = other_note.get_note_name()
		# Check lengths of names are the same
		if len(self._note_name) != len(other_note_name):
			return False
		# Check if each character is the same
		for num in range(len(self._note_name)):
			if self._note_name[num] != other_note_name[num]:
				return False

		return True

	def __ne__(self, other_note):
		"""
		Returns True if the notes are not equal, True otherwise.
		Again, Bb and A# are not the same note.
		"""
		return not self.__eq__(other_note)

	def __lt__(self, other_note):
		"""
		Returns True if the pitch of the first note (self) is lower than the pitch
		of the second note (other_note). Compares the notes enharmonically (Bb and
		A# are the same)
		"""
		other_note_number = other_note.get_midi_number()
		self_other_note_number = self.get_midi_number()
		return self_other_note_number < other_note_number

	def __gt__(self, other_note):
		"""
		Returns True if the pitch of the first note (self) is higher than the pitch
		of the second note (other_note). Compares the notes enharmonically (Bb and
		A# are the same)
		"""
		other_note_number = other_note.get_midi_number()
		self_other_note_number = self.get_midi_number()
		return self_other_note_number > other_note_number

	def __le__(self, other_note):
		"""
		Returns True if the pitch of the first note (self) is lower than the pitch
		of the second note (other_note) or equal (enharmonically). Compares the notes
		enharmonically (Bb and A# are the same)
		"""
		other_note_number = other_note.get_midi_number()
		self_other_note_number = self.get_midi_number()
		return self_other_note_number <= other_note_number

	def __ge__(self, other_note):
		"""
		Returns True if the pitch of the first note (self) is higher than the pitch
		of the second note (other_note) or equal (enharmonically). Compares the notes
		enharmonically (Bb and A# are the same)
		"""
		other_note_number = other_note.get_midi_number()
		self_other_note_number = self.get_midi_number()
		return self_other_note_number >= other_note_number

	def get_note_name(self):
		"""
		Returns a copy of the name of the pitch (without octave)
		"""
		return str(self._note_name)

	def get_octave(self):
		"""
		Returns a copy of the numerical value of the octave of the note.
		"""
		return int(self._octave)

	def get_note_number(self):
		"""
		Returns a copy of the pitch number of the note.
		"""
		return int(self._note_number)

	def get_note(self):
		"""
		Returns a deep copy of the note.
		"""
		return Note(str(self._note_name), int(self._octave))

	def get_midi_number(self):
		"""
		Returns the MIDI number corresponding to the note given.
		"""
		return self.get_note_number() + ((self.get_octave() + 1) * 12)

BASS_REGISTER_MIN = Note("D", 2)
BASS_REGISTER_MAX = Note("C", 4)
TENOR_REGISTER_MIN = Note("D", 3)
TENOR_REGISTER_MAX = Note("F", 4)
ALTO_REGISTER_MIN = Note("A", 3)
ALTO_REGISTER_MAX = Note("D", 5)
SOPR_REGISTER_MIN = Note("D", 4)
SOPR_REGISTER_MAX = Note("G", 5)

CHORD_QUALITY_TO_STRUCTURE = {"Maj": 47, "Maj6": 38, "Maj64": 59,
"Min": 37, "Min6": 49, "Min64": 58, "Aug": 48, "Aug6": 48, "Aug64": 48,
"Dim": 36, "Dim6": 39, "Dim64": 69, "Dom7": 4710, "Dom65": 368,
"Dom43": 359, "Dom42": 269}

CHORD_QUALITY_TO_INVERSION = {"Maj": 0, "Maj6": 1, "Maj64": 2,
"Min": 0, "Min6": 1, "Min64": 2, "Aug": 0, "Aug6": 1, "Aug64": 2,
"Dim": 0, "Dim6": 1, "Dim64": 2, "Dom7": 0, "Dom65": 1,
"Dom43": 2, "Dom42": 3}

def _check_notes_in_range(notes):
	"""
	Checks that the given notes are valid for a standard 4-part choir.
	"""
	if (notes[0] < BASS_REGISTER_MIN) or (notes[0] > BASS_REGISTER_MAX):
		raise TypeError, str(notes[0]) + " is not a valid not for a bass"
	if (notes[1] < TENOR_REGISTER_MIN) or (notes[1] > TENOR_REGISTER_MAX):
		raise TypeError, str(notes[1]) + " is not a valid not for a tenor"
	if (notes[2] < ALTO_REGISTER_MIN) or (notes[2] > ALTO_REGISTER_MAX):
		raise TypeError, str(notes[2]) + " is not a valid not for an alto"
	if (notes[3] < SOPR_REGISTER_MIN) or (notes[3] > SOPR_REGISTER_MAX):
		raise TypeError, str(notes[3]) + " is not a valid not for a soprano"

def get_chord_number(notes):
	"""
	Given a list of 4 notes, determines the chord structure based upon
	the mod 12 system of notes and the root. For example, C, E, and G
	are represented as a 0-4-7, and C#, E#, and G# is also 0-4-7.
	The chord structure is represented as an integer, so in this case, 047, or 47.
	"""
	root = notes[0].get_note_number()
	note1 = notes[1].get_note_number()
	note2 = notes[2].get_note_number()
	note3 = notes[3].get_note_number()

	note1 = (note1 - root) % 12
	note2 = (note2 - root) % 12
	note3 = (note3 - root) % 12

	lst1 = []
	if note1 != 0:
		lst1.append(note1)
	if note2 not in lst1 and note2 != 0:
		lst1.append(note2)
	if note3 not in lst1 and note3 != 0:
		lst1.append(note3)
	lst1.sort()

	lst2 = []
	for item in lst1:
		lst2.append(str(item))

	return int("".join(lst2))

def _check_chord_matches_notes(notes, quality):
	"""
	Checks if the given notes are of structure matching the given
	chord quality, and checks if given quality is valid.
	"""
	if quality not in CHORD_QUALITY_TO_STRUCTURE:
		raise TypeError, str(quality) + " is not a valid chord quality"

	chord_number1 = get_chord_number(notes)
	chord_number2 = CHORD_QUALITY_TO_STRUCTURE[quality]

	if chord_number2 != chord_number1:
		raise TypeError, str(quality) + " does not match the given notes"

class Chord:
	"""
	A chord in traditional 4-part harmony, which can be either a triad or 
	a seventh chord. Each chord (in this implementation) consists of four notes
	and its quality (in form of a string with figured bass (e.g. Maj6)).
	Each note is stored as the bass, tenor, alto, or soprano note based 
	on order entered (bass first).
	"""

	def __init__(self, note1, note2, note3, note4, quality):
		notes = [note1, note2, note3, note4]

		# Uncomment this to make input order not matter
		# notes.sort()

		_check_notes_in_range(notes)
		_check_chord_matches_notes(notes, quality)

		self._bass = notes[0].get_note()
		self._tenor = notes[1].get_note()
		self._alto = notes[2].get_note()
		self._sopr = notes[3].get_note()
		self._quality = str(quality)

	def __str__(self):
		string = "A " + self._quality + " Chord:"
		string = string + "\nSoprano: " + self._sopr.__str__()
		string = string + "\nAlto: " + self._alto.__str__()
		string = string + "\nTenor: " + self._tenor.__str__()
		string = string + "\nBass: " + self._bass.__str__()
		return string

	def get_bass(self):
		return self._bass.get_note()

	def get_tenor(self):
		return self._tenor.get_note()

	def get_alto(self):
		return self._alto.get_note()

	def get_sopr(self):
		return self._sopr.get_note()

	def get_notes(self):
		return [self._bass.get_note(), self._tenor.get_note(),
			self._alto.get_note(), self._sopr.get_note()]

	def get_chord(self):
		return Chord(self._bass.get_note(), self._tenor.get_note(),
			self._alto.get_note(), self._sopr.get_note(), str(self._quality))

def get_chord_notes(quality, root):
	"""
	Given a chord quality and a root note, the notes of the chord are
	returned outside of octave context, and outputted in the form of a list
	of string representations of notes.
	"""
	chord_number = str(CHORD_QUALITY_TO_STRUCTURE[quality])
	root_number = root.get_note_number()

	# notes is a list of the numeric representations of each
	# pitch in the code
	notes = [root_number]
	if len(chord_number) == 4: # For the special Dom7 Case (4710)
		notes.append((4 + root_number) % 12)
		notes.append((7 + root_number) % 12)
		notes.append((10 + root_number) % 12)
	else:
		for num in chord_number:
			notes.append((int(num) + root_number) % 12)

	# note_names is a list of the letters that each note will start with
	# (thus, no sharps or flats)
	root_name = root.get_note_name()

	note_names = [root_name[0]]
	index = SCALE_NOTES.find(root_name[0])
	inv = CHORD_QUALITY_TO_INVERSION[quality]

	if len(notes) == 3:  # To deal with Triads
		if inv == 0:
			note_names.append(SCALE_NOTES[index + 2])
			note_names.append(SCALE_NOTES[index + 4])
		elif inv == 1:
			note_names.append(SCALE_NOTES[index + 2])
			note_names.append(SCALE_NOTES[index + 5])
		else:
			note_names.append(SCALE_NOTES[index + 3])
			note_names.append(SCALE_NOTES[index + 5])

	else:  # To deal with seventh chords
		if inv == 0:
			note_names.append(SCALE_NOTES[index + 2])
			note_names.append(SCALE_NOTES[index + 4])
			note_names.append(SCALE_NOTES[index + 6])
		elif inv == 1:
			note_names.append(SCALE_NOTES[index + 2])
			note_names.append(SCALE_NOTES[index + 4])
			note_names.append(SCALE_NOTES[index + 5])
		elif inv == 2:
			note_names.append(SCALE_NOTES[index + 2])
			note_names.append(SCALE_NOTES[index + 3])
			note_names.append(SCALE_NOTES[index + 5])
		else:
			note_names.append(SCALE_NOTES[index + 1])
			note_names.append(SCALE_NOTES[index + 3])
			note_names.append(SCALE_NOTES[index + 5])

	result_notes = []

	# Finds the note name that matches the letter and the numerical
	# value. Can sometimes be double flats or sharps.
	for count in range(len(notes)):
		for key, value in PITCH_MAPPING.items():
			if key[0] == note_names[count]:
				if value == notes[count]:
					result_notes.append(key)

	return result_notes

def get_interval(note1, note2):
	"""
	Determines the melodic/harmonic interval from the first note up
	or down to the second note, returns in the form of the interval as an 
	integer (e.g. 7 for a 5th, 2 for a major 2nd). Always positive, and between
	0 and 11.
	"""
	if note1 >= note2 and note1 <= note2: #Accounts for enharmonics
		return 0

	if note1 > note2:
		high_note_pitch = note1.get_note_number()
		low_note_pitch = note2.get_note_number()
	else:
		high_note_pitch = note2.get_note_number()
		low_note_pitch = note1.get_note_number()

	if high_note_pitch > low_note_pitch:
		return high_note_pitch - low_note_pitch

	else:
		return (high_note_pitch - low_note_pitch) % 12

def get_nearest_note(current_note, next_note_name,
	min_note = Note("C", 0), max_note = Note("B", 9)):
	"""
	Given a current note and the name of the next note,
	returns the nearest version of that note in the given register limits.
	Register limit defaults to any note in given system.
	"""
	current_octave = current_note.get_octave()

	poss_notes = []
	if current_octave > 0:
		poss_notes.append(Note(next_note_name, current_octave - 1))
	poss_notes.append(Note(next_note_name, current_octave))
	if current_octave < 9:
		poss_notes.append(Note(next_note_name, current_octave + 1))

	min_int = float("inf")
	for note in poss_notes:
		if (note >= min_note) and (note <= max_note):
			if get_interval(note, current_note) <= min_int:
				next_note = note.get_note()

	return next_note.get_note()

def has_parallels(chord1, chord2):
	"""
	Returns True if there are parallel 5ths or octaves
	in the given two chords.
	"""
	notes1 = chord1.get_notes()
	notes2 = chord2.get_notes()
	for index_a, note_a in enumerate(notes1):
		for index_b, note_b in enumerate(notes1):
			if note_a != note_b:
				if get_interval(note_a, note_b) == get_interval(
					notes2[index_a], notes2[index_b]):
					if (get_interval(note_a, note_b) == 7) or (
						get_interval(note_a, note_b) == 0):
						return True
	return False

def has_voice_crossing(chord):
	"""
	Returns True if voices have crossed registers.
	"""
	bass = chord.get_bass()
	tenor = chord.get_tenor()
	alto = chord.get_alto()
	sopr = chord.get_sopr()

	return (bass > tenor) or (tenor > alto) or (alto > sopr)

def has_octave_gap(chord):
	"""
	Returns True if there is a gap between voices (excluding the bass) of
	more than an octave.
	"""
	tenor = chord.get_tenor()
	alto = chord.get_alto()
	sopr = chord.get_sopr()

	tenor_num = tenor.get_midi_number()
	alto_num = alto.get_midi_number()
	sopr_num = sopr.get_midi_number()

	return ((sopr_num - alto_num) > 12) or ((alto_num - tenor_num) > 12)

def has_doubled_leading_tone(chord, key):
	"""
	Returns True if the leading tone of the given key is doubled in the
	given chord and key, the key being a note name.
	"""
	key_num = PITCH_MAPPING[key]
	leading_tone_num = (key_num - 1) % 12

	count = 0
	chord_notes = chord.get_notes()
	for note in chord_notes:
		if note.get_note_number() == leading_tone_num:
			count += 1

	return count > 1

def evaluate_leaps(chord1, chord2):
	"""
	Returns the sum of the intervals between each voice (except the bass)
	sum is a number between 0 (no change except bass) and 33 (all major
	sevenths).
	"""
	total = 0
	notes1 = chord1.get_notes()
	notes2 = chord2.get_notes()
	# To eliminate the bass
	notes1.pop(0)
	notes2.pop(0)

	for note1, note2 in zip(notes1, notes2):
		total += get_interval(note1, note2)

	return total

def evaluate_progression(chord1, chord2, key):
	"""
	Returns a numerical representation of the quality of the progression.
	The higher the number, the more rules it violates, and the more 
	awkward the progression.
	"""
	total = 0.0
	# leaps are small problems, and unless there are a large number, they are fine
	total += (evaluate_leaps(chord1, chord2) / float(100))
	# voice crossing is worse than leaps
	if has_voice_crossing(chord2):
		total += .1
	# Octave gaps are even worse
	if has_octave_gap(chord2):
		total += .2
	# Doubled leading tones are not good.
	if has_doubled_leading_tone(chord2, key):
		total += .5
	# Parallel octaves and fifths are the worst.
	if has_parallels(chord1, chord2):
		total += 1

	return total

def get_next_chord(current_chord,next_quality,next_root_name,key,prev_chord=None):
	"""
	Generates the next chord in a progression, given the next
	chord's quality and the previous chord, along with the name of
	the next root (e.g. "F#"). The key of the progression must be given
	as well in order to ensure that the leading tone is never doubled.
	ALSO, MAYBE LATER ADD PREVIOUS CHORD FOR EXTRA CHECKS? MAYBE.
	"""
	# First, find the next bass note.
	current_bass = current_chord.get_bass()
	next_bass = get_nearest_note(current_bass, next_root_name, 
		BASS_REGISTER_MIN, BASS_REGISTER_MAX)

	# Now that the next bass is known, the needed notes can be determined
	chord_notes = get_chord_notes(next_quality, next_bass)
	needed_chord_notes = chord_notes[:]
	needed_chord_notes.remove(next_bass.get_note_name())
	
	# Now find all of the possible chords that contain these needed notes
	# For sevenths, no note is doubled, so using itertools, all possibilities
	# can be found.
	current_tenor = current_chord.get_tenor()
	current_alto = current_chord.get_alto()
	current_sopr = current_chord.get_sopr()
	poss_chords = []

	if len(needed_chord_notes) == 3:
		all_perms = list(itertools.permutations(needed_chord_notes))
		for needed_notes in all_perms:
			poss_chords.append(Chord(next_bass, 
				get_nearest_note(current_tenor, needed_notes[0], 
					TENOR_REGISTER_MIN, TENOR_REGISTER_MAX),
				get_nearest_note(current_alto, needed_notes[1], 
					ALTO_REGISTER_MIN, ALTO_REGISTER_MAX),
				get_nearest_note(current_sopr, needed_notes[2], 
					SOPR_REGISTER_MIN, SOPR_REGISTER_MAX),
				next_quality))

	# Triads are slightly more difficult to find all possible permutations, 
	# as up to one note can be repeated.
	elif len(needed_chord_notes) == 2:
		all_perms = []
		for note in chord_notes:
			for perm in list(itertools.permutations(needed_chord_notes)):
				for num in [0, 1, 2]:
					poss = list(perm)
					poss.insert(num, note)
					all_perms.append(poss)

		for needed_notes in all_perms:
			poss_chords.append(Chord(next_bass, 
				get_nearest_note(current_tenor, needed_notes[0], 
					TENOR_REGISTER_MIN, TENOR_REGISTER_MAX),
				get_nearest_note(current_alto, needed_notes[1], 
					ALTO_REGISTER_MIN, ALTO_REGISTER_MAX),
				get_nearest_note(current_sopr, needed_notes[2], 
					SOPR_REGISTER_MIN, SOPR_REGISTER_MAX),
				next_quality))

	# Now evaluate each of these possible chords using the rules in
	# evaluate_progression
	evaluations = []
	for chord in poss_chords:
		evaluations.append(evaluate_progression(current_chord, chord, key))

	# Now find the index of the lowest evaluation score
	min_eval = float("inf")
	for index, evaluation in enumerate(evaluations):
		if evaluation < min_eval:
			min_eval = evaluation
			min_index = index

	# print evaluations
	# print min_eval
	next_chord = poss_chords[min_index]
	# print evaluate_progression(current_chord, next_chord, key)
	return next_chord

ROMAN_NUMERAL_TO_QUALITY = {"I": ("Maj", 0), "I6": ("Maj6", 4), "I64": ("Maj64", 7),
"i": ("Min", 0), "i6": ("Min6", 3), "i64": ("Min64", 7), "ii": ("Min", 2),
"ii6": ("Min6", 5), "ii64": ("Min64", 9), "iidim": ("Dim", 2), "iidim6": ("Dim6", 5), 
"iidim64": ("Dim64", 8), "III": ("Maj", 3), "III6": ("Maj6", 7), "III64": ("Maj64", 10),
"iii": ("Min", 4), "iii6": ("Min6", 7), "iii64": ("Min64", 11), "IV": ("Maj", 5),
"IV6": ("Maj6", 9), "IV64": ("Maj64", 0), "iv": ("Min", 5), "iv6": ("Min6", 8),
"iv64": ("Min64", 0), "V": ("Maj", 7), "V6": ("Maj6", 11), "V64": ("Maj64", 2),
"V7": ("Dom7", 7), "V65": ("Dom65", 11), "V43": ("Dom43", 2), "V42": ("Dom42", 5),
"VI": ("Maj", 8), "VI6": ("Maj6", 0), "VI64": ("Maj64", 3), "vi": ("Min", 9),
"vi6": ("Min6", 0), "vi64": ("Min64", 4), "viidim": ("Dim", 11),
"viidim6": ("Dim6", 2), "viidim64": ("Dim64", 5)}

NOTE_NUM_TO_NUM_UP = {0: 0, 2: 1, 3: 2, 4: 2, 5: 3, 7: 4, 8: 5, 9: 5, 10: 6, 11: 6}

def get_first_chord(key, is_major):
	"""
	Determines the first chord of a progression.
	"""
	if is_major:
		qual = "Maj"
	else:
		qual = "Min"
	chord_notes = get_chord_notes(qual, Note(key, 2))

	bass = Note(key, 3)
	tenor = get_nearest_note(Note("Bb", 3), chord_notes[2], 
		TENOR_REGISTER_MIN, TENOR_REGISTER_MAX)		
	alto = get_nearest_note(Note("F", 4), chord_notes[1], 
		ALTO_REGISTER_MIN, ALTO_REGISTER_MAX)
	sopr = get_nearest_note(Note("B", 4), chord_notes[0], 
		SOPR_REGISTER_MIN, SOPR_REGISTER_MAX)

	return Chord(bass, tenor, alto, sopr, qual)

def get_root_name(roman_numeral, key):
	"""
	Determines the name of the root of a chord given the key and
	a roman numeral.
	"""
	note_num = ROMAN_NUMERAL_TO_QUALITY[roman_numeral][1]
	note_names_up = NOTE_NUM_TO_NUM_UP[note_num]

	note_letter = SCALE_NOTES[SCALE_NOTES.find(key[0]) + note_names_up]
	key_num = PITCH_MAPPING[key]
	note_num = (key_num + note_num) % 12

	for keya, value in PITCH_MAPPING.items():
		if value == note_num:
			if keya[0] == note_letter:
				return keya

def get_chord_progression(progression, key, is_major):
	"""
	Given a list of chords in roman numeral form, returns
	a list of chords that fit the progression. is_major is a boolean
	"""
	chords = []
	last_chord = get_first_chord(key, is_major)
	chords.append(last_chord)

	for numeral in progression[1:]:
		last_chord = get_next_chord(last_chord,
			ROMAN_NUMERAL_TO_QUALITY[numeral][0],
			get_root_name(numeral, key), key)
		chords.append(last_chord)

	return chords

# MAYBE TWEAK SO THAT GET_NEXT_CHORD TAKES PROGRESSION INSTEAD OF
# CURRENT_CHORD, AND CHECKS FOR TOO MUCH PARALLELS
# ALSO, ADD EVALUATION TO MAKE HALF STEP MOTION MORE COMMON. MAYBE IN
# EVALUATE LEAPS?

### Export as a midi using midiutil

from midiutil.MidiFile3 import MIDIFile

def create_midi_from_progression(progression):
	"""
	Given a chord progression in the form of a list of chord instances,
	creates a MIDI file as an output.
	"""
	MyMIDI = MIDIFile(4)
	track = 0
	time = 0
	MyMIDI.addTrackName(track, time, "Soprano")
	MyMIDI.addTempo(track, time, 60)
	track += 1
	MyMIDI.addTrackName(track, time, "Alto")
	MyMIDI.addTempo(track, time, 60)
	track += 1
	MyMIDI.addTrackName(track, time, "Tenor")
	MyMIDI.addTempo(track, time, 60)
	track += 1
	MyMIDI.addTrackName(track, time, "Bass")
	MyMIDI.addTempo(track, time, 60)

	channel = 0
	duration = 1
	volume = 100

	for index, chord in enumerate(progression):
		track = 3
		for note in chord.get_notes():
			pitch = note.get_midi_number()
			MyMIDI.addNote(track, channel, pitch, time, duration, volume)
			track -= 1
		time += 1
		if index == len(progression) - 2:
			duration = 2
	binfile = open("output_individual_voices.mid", 'wb')
	MyMIDI.writeFile(binfile)
	binfile.close()


	MyMIDI = MIDIFile(2)
	track = 0
	time = 0
	MyMIDI.addTrackName(track, time, "Upper Voices")
	MyMIDI.addTempo(track, time, 60)
	track += 1
	MyMIDI.addTrackName(track, time, "Lower Voices")
	MyMIDI.addTempo(track, time, 60)

	duration = 1

	for index, chord in enumerate(progression):
		track = 1
		count = 0
		for note in chord.get_notes():
			pitch = note.get_midi_number()
			MyMIDI.addNote(track, channel, pitch, time, duration, volume)
			if count % 2 == 1:
				track -= 1
			count += 1
		time += 1
		if index == len(progression) - 2:
			duration = 2
	binfile = open("output_two_hands.mid", 'wb')
	MyMIDI.writeFile(binfile)
	binfile.close()

# chords = get_chord_progression(["I", "viidim6", "I6", "vi", "ii", "IV6", "ii6", "IV", "V42", "I6", "V", "vi", "ii", "IV", "I64", "V7", "I"], "C", True)
# chords = get_chord_progression(["I", "IV6", "I6", "ii6", "V65", "vi", "ii6", "I64", "V7", "I"], "F", True)

# count = 1
# for chord in chords:
#  	print "Chord:", count
#  	print chord
#  	print
#  	count += 1

# create_midi_from_progression(chords)

### Generate a random sequence of Chords given a first order markov
### model representation of chord progressions

def next_state(markov_model, current_state):
    """
    Given a markov chain and the current state, randomly chooses
    the next state based upon the markov chain.
    """
    if markov_model:
        if current_state in markov_model:
            rand = random.random()
            for key, value in markov_model[current_state].items():
                if value > rand:
                    return key
                else:
                    rand -= value
    string = "ERROR:" + current_state + " NOT IN MODEL"
    return string

MAJOR_MARKOV_PROGRESSION_MODEL = {None: {"I": 1},
"I": {"V": .05, "IV": .15, "ii": .05, "ii6": .1, "viidim6": .15,
	"V42": .15, "iii": .025, "IV6": .075, None: .25},
"I6": {"V": .025, "IV": .2, "ii": .2, "ii6": .1, "IV6": .05, "V7": .025, 
	"V6": .05, "vi": .15, "iii": .15, "iii6": .05},
"I64": {"V": .3, "V7": .5, "vi": .15, "IV6": .05},
"ii": {"iii": .05, "iii6": .1, "IV": .3, "V": .05, "V7": .05, "V6": .05, "V65": .05,
	"V43": .05, "V42": .05, "vi": .05, "viidim": .05, "viidim6": .05, "I64": .1},
"ii6": {"iii": .05, "iii6": .1, "IV": .1, "V": .15, "V7": .15, "V6": .05, "V65": .05,
	"V43": .05, "V42": .05, "vi": .05, "viidim": .05, "viidim6": .05, "I64": .1},
"iii": {"vi": .6, "IV6": .1, "IV": .1, "ii": .1, "ii6": .1},
"iii6": {"vi": .4, "vi6": .4, "IV6": .1, "ii": .1},
"IV": {"I": .2, "V": .3, "V7": .3, "I64": .2},
"IV6": {"I": .05, "V": .35, "I6": .6},
"V": {"I": .5, "vi": .4, "IV6": .1},
"V6": {"I6": .6, "I": .2, "iii": .2},
"V7": {"I": .5, "vi": .4, "IV6": .1},
"V65": {"I": .3, "vi": .65, "IV6": .05},
"V43": {"I6": .4, "iii": .3, "vi": .4},
"V42": {"I6": .6, "I": .1, "V": .3},
"vi": {"ii": .5, "ii6": .3, "IV": .2},
"vi6": {"ii": .3, "ii6": .4, "IV": .3},
"viidim": {"iii": .4, "I6": .2, "V": .4},
"viidim6": {"I": .3, "I6": .6, "iii6": .1}}

def run(is_major=True):
	"""
	Runs a markov model of a harmonic progression. Currently only does major.
	"""
	### Randomly choose the chord qualities
	if is_major:
		markov = MAJOR_MARKOV_PROGRESSION_MODEL
	progression = [next_state(markov, None)]
	# count = 0
	while (progression[-1] != None):
		progression.append(next_state(markov, progression[-1]))
		print progression[-1]
		# count += 1
	progression.pop()

	### Randomly choose a key

	# I FORGOT HOW. DO THIS LATER.
	key = "C"

	### Generate the chord progression

	chords = get_chord_progression(progression, key, is_major)

	### Generate the MIDI files

	create_midi_from_progression(chords)


run()

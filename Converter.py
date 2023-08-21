import mido
import sys

def midi_note_to_frequency(midi_note):
    return 440 * (2 ** ((midi_note - 69) / 12))

def generate_powershell_script(midi_file_path, powershell_script_path):
    mid = mido.MidiFile(midi_file_path)
    
    powershell_code = []
    
    current_time = 0
    note_start_time = 0
    
    for msg in mid.play():
        current_time += msg.time
        if msg.type == 'note_on':
            note_pitch = msg.note
            note_frequency = midi_note_to_frequency(note_pitch)
            note_duration_seconds = current_time - note_start_time
            note_start_time = current_time
            
            print(f"Converting MIDI note {note_pitch} to frequency {int(note_frequency)} Hz")
            
            powershell_code.append(f'[console]::beep({int(note_frequency)}, {int(note_duration_seconds * 1000)})')

    with open(powershell_script_path, 'w') as powershell_script:
        powershell_script.write('\n'.join(powershell_code))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python midi_to_powershell.py input.mid output.ps1")
        sys.exit(1)
    
    input_midi_file = sys.argv[1]
    output_powershell_script = sys.argv[2]
    
    print("Generating PowerShell script...")
    generate_powershell_script(input_midi_file, output_powershell_script)
    print("PowerShell script generated successfully!")

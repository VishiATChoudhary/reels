HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p05-clarke
for f in clarke earth sat fibre call2 phone telex mf1961 switchboard telstar; do ln -sf ../../ep02/raw/$f.mp4 raw/$f.mp4; done
get rush     lJLQCMtt_5o   # 1960s London at rush hour, 16mm (Kinolibrary)
get bridge   7sDrJhM0oJg   # Crowds over London Bridge, 1968 (British Pathe)
get waterloo YVZIAlAz5qw   # 1960s Waterloo station interior, commuters (Kinolibrary)
get tube     hZ__S5aTLek   # 1960s London Tube, 16mm (Kinolibrary)
get tahiti   0V1ePNiQNd8   # 1960s Tahiti, black sand beach, 8mm (Kinolibrary)
get bali     vTDEsA9hwe4   # Bali beach, drone, free stock
get edin     meWDhviBe-8   # New surgical unit in Edinburgh hospital, 1960 (British Pathe)
get surgery  xssUFJYQe-4   # 1960s UK operating theatre, surgeons (Kinolibrary)
get fair     TLWuwdNgUOM   # New York World's Fair 1964, where Horizon filmed Clarke
get plane    dBgudVUoiFk   # view from a plane window, free stock
[ -f vo.wav ] || python3 "$HERE/p05-clarke.vo.py"
python3 "$HERE/p05-clarke.edit.py"

CL="crop=1080:1080:440:0"        # inside the 4:3 pillarbox, clear of the BBC bug
KINO="crop=570:570:170:0"        # Kinolibrary 720p: left of the K logo, above the burnt-in timecode
PATHE="crop=480:480:40:0"        # British Pathe / Kino 4:3 SD: left of the logo
SW="crop=720:720:280:0"          # switchboard: inside the pillarbox
TS="crop=360:360:140:30"         # telstar: above the burnt-in subtitles
shot clarke_hook clarke      136.12 2.4 "$WARM"  square "$CL"
shot sat         sat         6.2    2.7 "$COLD"  square
shot operators   switchboard 9.5    2.7 "$BLEAK" square "$SW"
shot tahiti      tahiti      22.0   2.7 "$TEAL"  square "$KINO"
shot bus         rush        15.0   2.7 "$COLD"  square "$KINO"
shot clarke_a    clarke      160.74 2.7 "$WARM"  square "$CL"
shot surgeons    surgery     5.0    2.7 "$TEAL"  square "$PATHE"
shot edinburgh   edin        40.5   1.9 "$BLEAK" square "$PATHE"
shot masks       surgery     9.8    1.9 "$COLD"  square "$PATHE"
shot theatre     surgery     17.35  1.9 "$TEAL"  square "$PATHE"
shot beams       telstar     54.5   1.9 "$TEAL"  square "$TS"
shot earth       earth       3.0    2.7 "$COLD"  square
shot bridge      bridge      2.0    1.1 "$BLEAK" square "$PATHE"
shot tube        tube        7.7    1.1 "$COLD"  square "$KINO"
shot crowd       rush        19.6   1.1 "$TEAL"  square "$KINO"
shot waterloo    waterloo    4.0    0.7 "$BLEAK" square "$KINO"
shot train       tube        48.6   0.7 "$COLD"  square "$KINO"
shot faces       rush        53.9   0.7 "$TEAL"  square "$KINO"
shot bridge2     bridge      10.0   0.7 "$COLD"  square "$PATHE"
shot fibre       fibre       2.0    1.1 "$VIVID" square
shot call        call2       5.0    1.1 "$AMBER" square
shot phone       phone       3.0    1.1 "$TEAL"  square
shot clarke_b    clarke      190.45 1.1 "$WARM"  square "$CL"
shot plane       plane       2.0    1.1 "$AMBER" square
shot bali        bali        25.0   1.1 "$VIVID" square
shot waves       tahiti      26.6   1.1 "$TEAL"  square "$KINO"
shot bali2       bali        50.0   1.1 "$AMBER" square
shot clarke_end  clarke      169.75 1.9 "$WARM"  square "$CL"

HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p09-hassabis
# hHooQmmzG4k: "Accelerating Scientific Discovery with AI", Demis Hassabis, Cambridge Computer Lab; section 1590 s on
[ -f raw/lecture.mp4 ] || "${YT[@]}" --download-sections "*1590-1800" -f "137+140/$FMT" --merge-output-format mp4 -o "raw/lecture.%(ext)s" -- hHooQmmzG4k
# P_fHJIYENdI: Veritasium, "AlphaFold - The Most Useful Thing AI Has Ever Done" (archive, charts, protein renders)
[ -f raw/veritasium.mp4 ] || "${YT[@]}" -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o "raw/veritasium.%(ext)s" -- P_fHJIYENdI
for f in sixty alphafold dc dna dna2 fold lab micro2 pipette; do ln -sf ../../ep08/raw/$f.mp4 raw/$f.mp4; done
if [ ! -f raw/src16.csv ]; then
  ffmpeg -v error -y -i raw/lecture.mp4 -vn -ar 16000 -ac 1 raw/src16.wav
  whisper-cli -m "$MODEL" -f raw/src16.wav -ml 1 -sow -ocsv -of raw/src16 -np >/dev/null 2>&1
fi
if [ ! -f raw/s60.csv ]; then
  ffmpeg -v error -y -ss 650 -t 30 -i raw/sixty.mp4 -vn -ar 16000 -ac 1 raw/s60.wav
  whisper-cli -m "$MODEL" -f raw/s60.wav -ml 1 -sow -ocsv -of raw/s60 -np >/dev/null 2>&1
fi
[ -f vo.wav ] || python3 "$HERE/p09-hassabis.vo.py"
python3 "$HERE/p09-hassabis.edit.py"

LEC="crop=520:520:1400:200"; FOLD="crop=iw-240:ih-130:240:0"  # FOLD: drops the amino acid counter
shot lec_hook   lecture    35.42  1.9 "$WARM"  square "$LEC"
shot biologist  lab        56.0   2.6 "$COLD"  square
shot student    micro2     2.0    2.6 "$BLEAK" square
shot kendrew    veritasium 144.7  2.6 "$BLEAK" square
shot oneprot    fold       30.0   2.6 "$COLD"  square "$FOLD"
shot many       dna2       10.0   2.6 "$TEAL"  square
shot lec_a      lecture    50.28  1.7 "$WARM"  square "$LEC"
shot afscreen   alphafold  55.0   2.0 "$TEAL"  square
shot screen60   sixty      627.0  1.8 "$COLD"  square
shot team       alphafold  65.0   1.8 "$TEAL"  square
shot servers    dc         30.0   1.8 "$COLD"  square
shot chart      veritasium 1166.5 1.1 "$TEAL"  square
shot spike      veritasium 1177.0 1.1 "$COLD"  square "crop=1080:1080:820:0"
shot cages      veritasium 1265.0 1.1 "$COLD"  square
shot sphere     veritasium 1272.5 1.1 "$TEAL"  square
shot grid       veritasium 75.0   0.7 "$COLD"  square
shot helix      dna2       20.0   0.7 "$COLD"  square
shot dc2        dc         40.0   0.7 "$TEAL"  square
shot fold2      fold       36.0   0.7 "$COLD"  square "$FOLD"
shot burst      dna        9.0    1.1 "$VIVID" square
shot pipette    pipette    3.0    1.1 "$AMBER" square
shot rainbow    veritasium 1277.0 1.1 "$VIVID" square
shot afprot     alphafold  165.0  1.1 "$AMBER" square
shot zoomcall   alphafold  405.0  1.1 "$RED"   square
shot hassabis60 sixty      665.45 1.8 "$WARM"  square
shot syringe    veritasium 1193.5 1.1 "$AMBER" square
shot mosquito   veritasium 1191.0 1.1 "$RED"   square
shot mri        veritasium 1203.0 1.1 "$TEAL"  square
shot rainbow2   veritasium 1279.5 1.1 "$VIVID" square
shot medal      sixty      602.5  2.6 "$WARM"  square

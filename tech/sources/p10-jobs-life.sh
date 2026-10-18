HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../tools/lib.sh"
ep tech p10-jobs-life
get jobs     kYfNvmF0Bqw              # Steve Jobs Secrets of Life (Silicon Valley Historical Association, 1994)
get class    ejzh1gbGdgI              # 1950s children in a London primary school
get rush     p5WX1Rm5k0Y              # 1950s early morning in London, commuters (Kinolibrary)
get cubicle  8foM-13y5w8              # 1982 office cubicles, Prudential Building (Kinolibrary)
get maze     qbL3c_Yxv0o 0:00-5:00    # Motivation and Reward in Learning (Yale, 1948): rats in boxes
get goldfish ad7kRaATVV4              # goldfish in a bowl
get esb      hUH1h6arQxo              # Empire State Building construction, 1930
get nyc      U3_uxUSeZV4 0:00-2:30    # New York timelapse and hyperlapse (Michael Shainblum)
get mac84    2B-XwPjn9YY              # Jobs introduces the Macintosh, January 1984
ln -sf ../../p05-clarke/raw/earth.mp4 raw/earth.mp4
ln -sf ../../p03-feynman/raw/wright.mp4 raw/wright.mp4
for f in apple2 board apple2ad; do ln -sf ../../ep04/raw/$f.mp4 raw/$f.mp4; done
[ -f vo.wav ] || python3 "$HERE/p10-jobs-life.vo.py"
python3 "$HERE/p10-jobs-life.edit.py"

# archive crops keep the burnt-in timecodes and library logos out of the square (ESB: y < 780 clears the Buyout mark)
CLASS="crop=380:380:130:30"; RUSH="crop=540:540:370:0"; CUBE="crop=370:370:240:0"
shot jobs_hook jobs     13.35  1.6 "$WARM"  square
shot class     class    23.0   2.3 "$BLEAK" square "$CLASS"
shot earth     earth    2.0    2.3 "$COLD"  square
shot rush      rush     66.0   2.3 "$BLEAK" square "$RUSH"
shot cubicle   cubicle  1.0    2.3 "$COLD"  square "$CUBE"
shot rat       maze     204.0  2.3 "$BLEAK" square
shot goldfish  goldfish 4.0    2.3 "$TEAL"  square
shot jobs_a    jobs     34.29  1.8 "$WARM"  square
shot skyline   nyc      79.0   1.5 "$TEAL"  square
shot pedestal  mac84    80.5   1.6 "$COLD"  square
shot wright    wright   0.5    1.0 "$BLEAK" square
shot beam      esb      13.5   1.0 "$COLD"  square "crop=780:780:480:0"
shot apple2    apple2   5.0    0.7 "$COLD"  square
shot station   nyc      30.0   0.7 "$TEAL"  square
shot board     board    4.0    0.7 "$COLD"  square
shot aerial    nyc      18.0   0.7 "$TEAL"  square
shot cross     nyc      66.0   1.0 "$VIVID" square
shot times     nyc      37.0   1.0 "$AMBER" square
shot crowd     rush     70.0   1.0 "$VIVID" square "$RUSH"
shot beam2     esb      28.0   1.0 "$AMBER" square "crop=780:780:280:0"
shot beam3     esb      39.5   1.6 "$RED"   square "crop=780:780:180:0"
shot jobs_b    jobs     44.02  1.6 "$WARM"  square
shot apple1    apple2   135.0  1.6 "$VIVID" square
shot insanely  mac84    128.0  1.6 "$AMBER" square
shot open      apple2   160.0  1.6 "$TEAL"  square
shot paint     mac84    137.0  1.6 "$AMBER" square
shot girl      apple2ad 12.0   1.0 "$VIVID" square
shot cheer     mac84    268.0  1.6 "$RED"   square
shot jobs_end  jobs     94.505 2.3 "$WARM"  square
shot ovation   mac84    257.0  2.3 "$WARM"  square   # Jobs, silent, smiling into the 1984 ovation

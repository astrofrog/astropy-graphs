```
gource --logo-offset 1835x995 --logo astropy.png --title "Astropy Development" --hide dirnames,mouse,filenames  -1920x1080 --seconds-per-day 0.001 --auto-skip-seconds 1  --stop-at-end -o - | ffmpeg -y -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -preset ultrafast -pix_fmt yuv420p -crf 1 -threads 0 -bf 0 ~/tmp/gource/astropy.mp4
```

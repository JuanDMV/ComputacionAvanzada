unset multiplot
set term postscript eps enhanced color dashlength 0.5 "Helvetica" 30
set encoding utf8
set output "Omtiempos.ps"
set rmargin 0
set lmargin 0
set tmargin 0
set bmargin 0

unset key
set xrange[1:19]
set yrange[0:55]
set tics scale 2
set xtics out 3,3,18
set mxtics 4
set ytics out 0,5,55
set mytics 5
set size ratio 1
#set origin 0.2, 0.2
set pointsize 3.0
set xlabel "{/Symbol a}|E_i|^2" offset 0.5, 0.0
set ylabel "tiempo (s)" offset 1.5, -1.4

set label 1 "1 núcleo" at 2.87, 45 font "Helvetica, 25" front textcolor rgbcolor "black"
set label 2 "2 núcleos" at 15,28.7 font "Helvetica, 25" front textcolor rgbcolor "#cc0000"
set label 3 "3 núcleos" at 15, 18 font "Helvetica, 25" front textcolor rgbcolor "#094a85"
set label 4 "4 núcleos" at 12,8 font "Helvetica, 25" front textcolor rgbcolor "#82b807"
set label 5 "(b) " at 17.8, 2.3 font "Helvetica, 25" front textcolor rgbcolor "black"

plot "dat_omvalues.dat" u 1:2 w lp pt 5 lc rgb "black"
plot "dat_omvalues.dat" u 1:3 w lp pt 7 lc rgb "#cc0000"
plot "dat_omvalues.dat" u 1:4 w lp pt 9 lc rgb "#094a85"
plot "dat_omvalues.dat" u 1:5 w lp pt 13 lc rgb "#82b807"



unset multiplot
reset

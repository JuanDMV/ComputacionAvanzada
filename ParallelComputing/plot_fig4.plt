unset multiplot
set term postscript eps enhanced color dashlength 0.5 "Helvetica" 30
set encoding iso_8859_1
set output "Trvsomega.ps"
set rmargin 0
set lmargin 0
set tmargin 0
set bmargin 0

unset key
set xrange[0:300]
set yrange[0.2:1]
#set logscale y
set tics scale 2
set xtics out 0,50,300
set mxtics 5
set ytics out 0.2,0.1, 1
set mytics 2
set size ratio 1
set pointsize 0.3
set xlabel "{/Symbol w}" offset 0.5, 0.0
set ylabel "T" offset 2.5, 0.0

set label 1 "a = 3" at 4, 0.93 font "Helvetica, 25" front textcolor rgbcolor "black"
set label 2 "a = 6" at 86,0.245 font "Helvetica, 25" front textcolor rgbcolor "#cc0000"
set label 3 "a = 9" at 187, 0.235 font "Helvetica, 25" front textcolor rgbcolor "#094a85"
plot "Omvalues_3_np.dat" u 1:2 w p pt 7 lc rgb "black"
plot "Omvalues_6_np.dat" u 1:2 w p pt 7 lc rgb "#cc0000"
plot "Omvalues_9_np.dat" u 1:2 w p pt 7 lc rgb "#094a85"

unset multiplot

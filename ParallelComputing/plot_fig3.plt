unset multiplot
set term postscript eps enhanced color dashlength 0.5 "Helvetica" 30
set encoding iso_8859_1
set output "fig3.ps"
set rmargin 0
set lmargin 0
set tmargin 0
set bmargin 0

unset key
set xrange[-9:10]
set yrange[0.2:1]
set logscale y
set tics scale 2
set xtics out -9,3,10
set mxtics 3
set ytics out 0.2,0.1, 1 nolog
set mytics 2
set size ratio 1
#set origin 0.2, 0.2
set pointsize 0.2
set xlabel "{/Symbol a}|E_i|^2" offset 0.5, 0.0
set ylabel "T" offset 2.5, 0.0

set label 1 "N = 2" at 1, 0.9 font "Helvetica, 25" front textcolor rgbcolor "black"
set label 2 "N = 6" at -7,0.28 font "Helvetica, 25" front textcolor rgbcolor "#cc0000"
set label 3 "N = 10" at 4, 0.25 font "Helvetica, 25" front textcolor rgbcolor "#094a85"
plot "Alvalues_2_np.dat" u 1:2 w p pt 7 lc rgb "black"
plot "Alvalues_6_np.dat" u 1:2 w p pt 7 lc rgb "#cc0000"
plot "Alvalues_10_np.dat" u 1:2 w p pt 7 lc rgb "#094a85"
#plot "Alvalues_14_np.dat" u 1:2 w p pt 7 lc rgb "#326a1a"

unset multiplot

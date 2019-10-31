top=$1
for I in A B C D E F G
do
    for J in {1..10}
    do
        printf "%c%02d%c" $top $J $I
        echo " "
    done
done

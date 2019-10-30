top=$1
for I in A B C D E F G
do
    for J in {1..10}
    do
        printf "%c%2d%c" $top $J $I
    done
done

src=$1
tgt=$2
input_file=$3
bpe_file=bpe.$input_file

BPEROOT=~/research3.7/subword-nmt/subword_nmt
BPE_TOKENS=40000

mkdir -p $bpe_file
mv $input_file/*valid.$src $input_file/valid.$src
mv $input_file/*valid.$tgt $input_file/valid.$tgt
mv $input_file/*train.$src $input_file/train.$src
mv $input_file/*train.$tgt $input_file/train.$tgt
mv $input_file/*test.$src $input_file/test.$src
mv $input_file/*test.$tgt $input_file/test.$tgt

TRAIN=$bpe_file/train.both
BPE_CODE=$bpe_file/spm.model
rm -f $TRAIN
for l in $src $tgt; do
    cat $input_file/train.$l >> $TRAIN
done

echo "learn_bpe.py on ${TRAIN}..."
python $BPEROOT/learn_bpe.py -s $BPE_TOKENS < $TRAIN > $BPE_CODE

for L in $src $tgt; do
    for f in train.$L valid.$L test.$L; do
        echo "apply_bpe.py to ${f}..."
        python $BPEROOT/apply_bpe.py -c $BPE_CODE < $input_file/$f > $bpe_file/$f
    done
done

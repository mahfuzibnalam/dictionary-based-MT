src=$1
tgt=$2
input_file=$3
dict_file=/home/mahfuz/Research/MachineTranslation/DeltaLM/models/multi/vocab/dict.txt

fairseq-preprocess \
    --trainpref $input_file/train \
    --validpref $input_file/valid \
    --testpref $input_file/test \
    --source-lang $src \
    --target-lang $tgt \
    --destdir binarized.$input_file \
    --workers 80 \
    --srcdict $dict_file \
    --tgtdict $dict_file 

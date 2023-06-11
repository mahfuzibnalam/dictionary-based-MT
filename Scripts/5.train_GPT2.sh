train=$1
valid=$2
tokenizer=$3
output=$4

python ~/research3.7/transformers/examples/pytorch/language-modeling/run_clm.py \
    --model_type gpt2 \
    --train_file $train \
    --validation_file $valid \
    --config_name $tokenizer \
    --tokenizer_name $tokenizer \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --do_train \
    --do_eval \
    --output_dir $output \
    --save_total_limit 2 \
    --overwrite_output_dir

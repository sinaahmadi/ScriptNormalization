#!/bin/bash

# $1 clean
echo "Training the model..." $1
./fastText-0.9.2/fasttext  supervised -input $1/train.txt -output $1/model_langdetect -dim 16 -minn 2 -maxn 4 -loss hs
echo "Compressing..."
./fastText-0.9.2/fasttext quantize -input $1/train.txt -output $1/model_langdetect -qnorm -cutoff 50000 -retrain

echo "Testing the model..."
./fastText-0.9.2/fasttext test $1/model_langdetect.bin $1/test.txt
./fastText-0.9.2/fasttext test $1/model_langdetect.bin $1/test.txt 2
./fastText-0.9.2/fasttext test $1/model_langdetect.bin $1/test.txt 3
./fastText-0.9.2/fasttext test $1/model_langdetect.bin $1/test.txt 4

echo "Testing with lid.176..."
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin $1/test.txt
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin $1/test.txt 2
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin $1/test.txt 3
./fastText-0.9.2/fasttext test fastText-0.9.2/lid.176.bin $1/test.txt 4

./fastText-0.9.2/fasttext predict $1/model_langdetect.bin $1/test.txt 4 > $1/model_predict.txt
echo "Prediction done."
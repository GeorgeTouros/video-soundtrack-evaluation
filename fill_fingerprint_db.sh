#!/bin/bash
echo "Starting running python scripts"
source /home/zappatistas20/PycharmProjects/venvs/thesis_dataset_creation/bin/activate
TEMPDIR=/home/zappatistas20/PycharmProjects/thesis_dataset_creation/temp/audio/
cd $TEMPDIR;
COUNTER=$1
while [ $COUNTER -le $2 ]
do
	FOLD1="${TEMPDIR}audio_${COUNTER}"
	INCR=$((COUNTER+1))
	FOLD2="${TEMPDIR}audio_${INCR}"
	INCR2=$((COUNTER+2))
	FOLD3="${TEMPDIR}audio_${INCR2}"
	echo $FOLD1
	echo $FOLD2
	echo $FOLD3
	python /home/zappatistas20/PycharmProjects/thesis_dataset_creation/fingerprinter_cmd.py -T $FOLD1
	python /home/zappatistas20/PycharmProjects/thesis_dataset_creation/fingerprinter_cmd.py -T $FOLD2
	python /home/zappatistas20/PycharmProjects/thesis_dataset_creation/fingerprinter_cmd.py -T $FOLD3
	(( COUNTER ++ ))
	(( COUNTER ++ ))
	(( COUNTER ++ ))
	echo "==========> JUST FINISHED ==================="
done
echo All done

FROM python:3 AS py
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip setuptools
RUN python -m pip install --upgrade cython
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./main_word2vec.py" ]
# CMD ["cp", "./models/koala_word2lvec.bin" ""]
# COPY --from=py /models/koala_word2lvec.bin ./result.bin
# RUN id=$(docker create test)
# RUN docker cp $id:/models/koala_word2lvec.bin - > ./result.bin
# RUN docker rm -v $id


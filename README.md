original github link: https://github.com/gtolias/how

I Changed some file for evaluate the dataset I made, and is debugging now.
The dataset is about automobile mechanical drawings, aim to search for the same mechanical drawings.



## Running the Code

```
pip3 install pyaml numpy faiss-gpu
cd asmk
python3 setup.py build_ext --inplace
rm -r build
cd ..
export PYTHONPATH=${PYTHONPATH}:$(realpath asmk)
```

3. Install pip3 requirements

```
pip3 install -r requirements.txt
```

4. Run `examples/demo_how.py` with two arguments &ndash; mode (`train` or `eval`) and any `.yaml` parameter file from `examples/params/*/*.yml`
```
cd how/examples
python demo_how.py eval params/eccv20/eval_how_r50-_1000.yml -e official_how_r50-_1000 

```

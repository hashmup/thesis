#!/bin/sh
pullIfNotExist() {
    # NEURONの本体を拡張したneuron_kplusが存在しない場合はGithubからクローンする
    if [ ! -d "neuron_kplus" ]; then
        git clone git@github.com:hashmup/neuron_k.git neuron_kplus
        # NEURON-7.2 をビルドする際に必要となる空のディレクトリを明示的に追加する
        mkdir -p neuron_kplus/nrn-7.2/src/npy24
        mkdir -p neuron_kplus/nrn-7.2/src/npy25
        mkdir -p neuron_kplus/nrn-7.2/src/npy26
        mkdir -p neuron_kplus/nrn-7.2/src/npy27
    else
        # NEURON がすでに存在している場合は,NEURON を最新版に更新する
        (cd neuron_kplus &&
        git checkout . &&
        git pull origin master)
    fi
}
pullIfNotExist

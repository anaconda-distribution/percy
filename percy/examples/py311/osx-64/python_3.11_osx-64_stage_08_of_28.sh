#!/bin/bash
CONDA_ADD_PIP_AS_PYTHON_DEPENDENCY=0

if [[ ! -f cryptography-feedstock.mark ]]; then
    if [[ -d cryptography-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./cryptography-feedstock >d 2>&1 && rm -f d && ( echo "done" >>cryptography-feedstock.mark ) && true) || ( (echo "cryptography-feedstock" >>failed.8 ) && (echo "cryptography-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "cryptography-feedstock not present" >>failed.8
    fi
fi


if [[ ! -f setuptools_scm-feedstock.mark ]]; then
    if [[ -d setuptools_scm-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./setuptools_scm-feedstock >d 2>&1 && rm -f d && ( echo "done" >>setuptools_scm-feedstock.mark ) && true) || ( (echo "setuptools_scm-feedstock" >>failed.8 ) && (echo "setuptools_scm-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "setuptools_scm-feedstock not present" >>failed.8
    fi
fi

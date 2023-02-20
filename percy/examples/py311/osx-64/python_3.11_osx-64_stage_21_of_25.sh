#!/bin/bash
CONDA_ADD_PIP_AS_PYTHON_DEPENDENCY=0

if [[ ! -f aiohttp-feedstock.mark ]]; then
    if [[ -d aiohttp-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./aiohttp-feedstock >d 2>&1 && rm -f d && ( echo "done" >>aiohttp-feedstock.mark ) && true) || ( (echo "aiohttp-feedstock" >>failed.21 ) && (echo "aiohttp-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "aiohttp-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f altgraph-feedstock.mark ]]; then
    if [[ -d altgraph-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./altgraph-feedstock >d 2>&1 && rm -f d && ( echo "done" >>altgraph-feedstock.mark ) && true) || ( (echo "altgraph-feedstock" >>failed.21 ) && (echo "altgraph-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "altgraph-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f apispec-feedstock.mark ]]; then
    if [[ -d apispec-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./apispec-feedstock >d 2>&1 && rm -f d && ( echo "done" >>apispec-feedstock.mark ) && true) || ( (echo "apispec-feedstock" >>failed.21 ) && (echo "apispec-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "apispec-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f astroid-feedstock.mark ]]; then
    if [[ -d astroid-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./astroid-feedstock >d 2>&1 && rm -f d && ( echo "done" >>astroid-feedstock.mark ) && true) || ( (echo "astroid-feedstock" >>failed.21 ) && (echo "astroid-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "astroid-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f cachelib-feedstock.mark ]]; then
    if [[ -d cachelib-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./cachelib-feedstock >d 2>&1 && rm -f d && ( echo "done" >>cachelib-feedstock.mark ) && true) || ( (echo "cachelib-feedstock" >>failed.21 ) && (echo "cachelib-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "cachelib-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f coverage-feedstock.mark ]]; then
    if [[ -d coverage-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./coverage-feedstock >d 2>&1 && rm -f d && ( echo "done" >>coverage-feedstock.mark ) && true) || ( (echo "coverage-feedstock" >>failed.21 ) && (echo "coverage-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "coverage-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f dill-feedstock.mark ]]; then
    if [[ -d dill-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./dill-feedstock >d 2>&1 && rm -f d && ( echo "done" >>dill-feedstock.mark ) && true) || ( (echo "dill-feedstock" >>failed.21 ) && (echo "dill-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "dill-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f exceptiongroup-feedstock.mark ]]; then
    if [[ -d exceptiongroup-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./exceptiongroup-feedstock >d 2>&1 && rm -f d && ( echo "done" >>exceptiongroup-feedstock.mark ) && true) || ( (echo "exceptiongroup-feedstock" >>failed.21 ) && (echo "exceptiongroup-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "exceptiongroup-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f filesystem-spec-feedstock.mark ]]; then
    if [[ -d filesystem-spec-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./filesystem-spec-feedstock >d 2>&1 && rm -f d && ( echo "done" >>filesystem-spec-feedstock.mark ) && true) || ( (echo "filesystem-spec-feedstock" >>failed.21 ) && (echo "filesystem-spec-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "filesystem-spec-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f flask-jwt-extended-feedstock.mark ]]; then
    if [[ -d flask-jwt-extended-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./flask-jwt-extended-feedstock >d 2>&1 && rm -f d && ( echo "done" >>flask-jwt-extended-feedstock.mark ) && true) || ( (echo "flask-jwt-extended-feedstock" >>failed.21 ) && (echo "flask-jwt-extended-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "flask-jwt-extended-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f flask-login-feedstock.mark ]]; then
    if [[ -d flask-login-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./flask-login-feedstock >d 2>&1 && rm -f d && ( echo "done" >>flask-login-feedstock.mark ) && true) || ( (echo "flask-login-feedstock" >>failed.21 ) && (echo "flask-login-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "flask-login-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f flask-sqlalchemy-feedstock.mark ]]; then
    if [[ -d flask-sqlalchemy-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./flask-sqlalchemy-feedstock >d 2>&1 && rm -f d && ( echo "done" >>flask-sqlalchemy-feedstock.mark ) && true) || ( (echo "flask-sqlalchemy-feedstock" >>failed.21 ) && (echo "flask-sqlalchemy-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "flask-sqlalchemy-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f flask-wtf-feedstock.mark ]]; then
    if [[ -d flask-wtf-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./flask-wtf-feedstock >d 2>&1 && rm -f d && ( echo "done" >>flask-wtf-feedstock.mark ) && true) || ( (echo "flask-wtf-feedstock" >>failed.21 ) && (echo "flask-wtf-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "flask-wtf-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f httpcore-feedstock.mark ]]; then
    if [[ -d httpcore-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./httpcore-feedstock >d 2>&1 && rm -f d && ( echo "done" >>httpcore-feedstock.mark ) && true) || ( (echo "httpcore-feedstock" >>failed.21 ) && (echo "httpcore-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "httpcore-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f inflection-feedstock.mark ]]; then
    if [[ -d inflection-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./inflection-feedstock >d 2>&1 && rm -f d && ( echo "done" >>inflection-feedstock.mark ) && true) || ( (echo "inflection-feedstock" >>failed.21 ) && (echo "inflection-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "inflection-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f jupyter_console-feedstock.mark ]]; then
    if [[ -d jupyter_console-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./jupyter_console-feedstock >d 2>&1 && rm -f d && ( echo "done" >>jupyter_console-feedstock.mark ) && true) || ( (echo "jupyter_console-feedstock" >>failed.21 ) && (echo "jupyter_console-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "jupyter_console-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f jupyterlab-feedstock.mark ]]; then
    if [[ -d jupyterlab-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./jupyterlab-feedstock >d 2>&1 && rm -f d && ( echo "done" >>jupyterlab-feedstock.mark ) && true) || ( (echo "jupyterlab-feedstock" >>failed.21 ) && (echo "jupyterlab-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "jupyterlab-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f mako-feedstock.mark ]]; then
    if [[ -d mako-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./mako-feedstock >d 2>&1 && rm -f d && ( echo "done" >>mako-feedstock.mark ) && true) || ( (echo "mako-feedstock" >>failed.21 ) && (echo "mako-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "mako-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f markdown-it-py-feedstock.mark ]]; then
    if [[ -d markdown-it-py-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./markdown-it-py-feedstock >d 2>&1 && rm -f d && ( echo "done" >>markdown-it-py-feedstock.mark ) && true) || ( (echo "markdown-it-py-feedstock" >>failed.21 ) && (echo "markdown-it-py-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "markdown-it-py-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f marshmallow-enum-feedstock.mark ]]; then
    if [[ -d marshmallow-enum-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./marshmallow-enum-feedstock >d 2>&1 && rm -f d && ( echo "done" >>marshmallow-enum-feedstock.mark ) && true) || ( (echo "marshmallow-enum-feedstock" >>failed.21 ) && (echo "marshmallow-enum-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "marshmallow-enum-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f matplotlib-feedstock.mark ]]; then
    if [[ -d matplotlib-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./matplotlib-feedstock >d 2>&1 && rm -f d && ( echo "done" >>matplotlib-feedstock.mark ) && true) || ( (echo "matplotlib-feedstock" >>failed.21 ) && (echo "matplotlib-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "matplotlib-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f pandas-feedstock.mark ]]; then
    if [[ -d pandas-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./pandas-feedstock >d 2>&1 && rm -f d && ( echo "done" >>pandas-feedstock.mark ) && true) || ( (echo "pandas-feedstock" >>failed.21 ) && (echo "pandas-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "pandas-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f param-feedstock.mark ]]; then
    if [[ -d param-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./param-feedstock >d 2>&1 && rm -f d && ( echo "done" >>param-feedstock.mark ) && true) || ( (echo "param-feedstock" >>failed.21 ) && (echo "param-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "param-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f prison-feedstock.mark ]]; then
    if [[ -d prison-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./prison-feedstock >d 2>&1 && rm -f d && ( echo "done" >>prison-feedstock.mark ) && true) || ( (echo "prison-feedstock" >>failed.21 ) && (echo "prison-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "prison-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f protobuf-feedstock.mark ]]; then
    if [[ -d protobuf-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./protobuf-feedstock >d 2>&1 && rm -f d && ( echo "done" >>protobuf-feedstock.mark ) && true) || ( (echo "protobuf-feedstock" >>failed.21 ) && (echo "protobuf-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "protobuf-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f pyobjc-framework-cocoa-feedstock.mark ]]; then
    if [[ -d pyobjc-framework-cocoa-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./pyobjc-framework-cocoa-feedstock >d 2>&1 && rm -f d && ( echo "done" >>pyobjc-framework-cocoa-feedstock.mark ) && true) || ( (echo "pyobjc-framework-cocoa-feedstock" >>failed.21 ) && (echo "pyobjc-framework-cocoa-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "pyobjc-framework-cocoa-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f qtconsole-feedstock.mark ]]; then
    if [[ -d qtconsole-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./qtconsole-feedstock >d 2>&1 && rm -f d && ( echo "done" >>qtconsole-feedstock.mark ) && true) || ( (echo "qtconsole-feedstock" >>failed.21 ) && (echo "qtconsole-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "qtconsole-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f ruamel-feedstock.mark ]]; then
    if [[ -d ruamel-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./ruamel-feedstock >d 2>&1 && rm -f d && ( echo "done" >>ruamel-feedstock.mark ) && true) || ( (echo "ruamel-feedstock" >>failed.21 ) && (echo "ruamel-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "ruamel-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f ruamel.yaml.clib-feedstock.mark ]]; then
    if [[ -d ruamel.yaml.clib-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./ruamel.yaml.clib-feedstock >d 2>&1 && rm -f d && ( echo "done" >>ruamel.yaml.clib-feedstock.mark ) && true) || ( (echo "ruamel.yaml.clib-feedstock" >>failed.21 ) && (echo "ruamel.yaml.clib-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "ruamel.yaml.clib-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f s3transfer-feedstock.mark ]]; then
    if [[ -d s3transfer-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./s3transfer-feedstock >d 2>&1 && rm -f d && ( echo "done" >>s3transfer-feedstock.mark ) && true) || ( (echo "s3transfer-feedstock" >>failed.21 ) && (echo "s3transfer-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "s3transfer-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f scipy-feedstock.mark ]]; then
    if [[ -d scipy-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./scipy-feedstock >d 2>&1 && rm -f d && ( echo "done" >>scipy-feedstock.mark ) && true) || ( (echo "scipy-feedstock" >>failed.21 ) && (echo "scipy-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "scipy-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f setuptools-git-versioning-feedstock.mark ]]; then
    if [[ -d setuptools-git-versioning-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./setuptools-git-versioning-feedstock >d 2>&1 && rm -f d && ( echo "done" >>setuptools-git-versioning-feedstock.mark ) && true) || ( (echo "setuptools-git-versioning-feedstock" >>failed.21 ) && (echo "setuptools-git-versioning-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "setuptools-git-versioning-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f sqlparse-feedstock.mark ]]; then
    if [[ -d sqlparse-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./sqlparse-feedstock >d 2>&1 && rm -f d && ( echo "done" >>sqlparse-feedstock.mark ) && true) || ( (echo "sqlparse-feedstock" >>failed.21 ) && (echo "sqlparse-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "sqlparse-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f twine-feedstock.mark ]]; then
    if [[ -d twine-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./twine-feedstock >d 2>&1 && rm -f d && ( echo "done" >>twine-feedstock.mark ) && true) || ( (echo "twine-feedstock" >>failed.21 ) && (echo "twine-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "twine-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f typing-feedstock.mark ]]; then
    if [[ -d typing-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./typing-feedstock >d 2>&1 && rm -f d && ( echo "done" >>typing-feedstock.mark ) && true) || ( (echo "typing-feedstock" >>failed.21 ) && (echo "typing-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "typing-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f uc-micro-py-feedstock.mark ]]; then
    if [[ -d uc-micro-py-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./uc-micro-py-feedstock >d 2>&1 && rm -f d && ( echo "done" >>uc-micro-py-feedstock.mark ) && true) || ( (echo "uc-micro-py-feedstock" >>failed.21 ) && (echo "uc-micro-py-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "uc-micro-py-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f ujson-feedstock.mark ]]; then
    if [[ -d ujson-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./ujson-feedstock >d 2>&1 && rm -f d && ( echo "done" >>ujson-feedstock.mark ) && true) || ( (echo "ujson-feedstock" >>failed.21 ) && (echo "ujson-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "ujson-feedstock not present" >>failed.21
    fi
fi


if [[ ! -f xyzservices-feedstock.mark ]]; then
    if [[ -d xyzservices-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./xyzservices-feedstock >d 2>&1 && rm -f d && ( echo "done" >>xyzservices-feedstock.mark ) && true) || ( (echo "xyzservices-feedstock" >>failed.21 ) && (echo "xyzservices-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "xyzservices-feedstock not present" >>failed.21
    fi
fi

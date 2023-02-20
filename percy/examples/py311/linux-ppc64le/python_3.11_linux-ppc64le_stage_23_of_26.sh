#!/bin/bash
CONDA_ADD_PIP_AS_PYTHON_DEPENDENCY=0

if [[ ! -f alembic-feedstock.mark ]]; then
    if [[ -d alembic-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./alembic-feedstock >d 2>&1 && rm -f d && ( echo "done" >>alembic-feedstock.mark ) && true) || ( (echo "alembic-feedstock" >>failed.23 ) && (echo "alembic-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "alembic-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f altgraph-feedstock.mark ]]; then
    if [[ -d altgraph-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./altgraph-feedstock >d 2>&1 && rm -f d && ( echo "done" >>altgraph-feedstock.mark ) && true) || ( (echo "altgraph-feedstock" >>failed.23 ) && (echo "altgraph-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "altgraph-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f apache-airflow-providers-common-sql-feedstock.mark ]]; then
    if [[ -d apache-airflow-providers-common-sql-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./apache-airflow-providers-common-sql-feedstock >d 2>&1 && rm -f d && ( echo "done" >>apache-airflow-providers-common-sql-feedstock.mark ) && true) || ( (echo "apache-airflow-providers-common-sql-feedstock" >>failed.23 ) && (echo "apache-airflow-providers-common-sql-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "apache-airflow-providers-common-sql-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f apache-airflow-providers-ftp-feedstock.mark ]]; then
    if [[ -d apache-airflow-providers-ftp-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./apache-airflow-providers-ftp-feedstock >d 2>&1 && rm -f d && ( echo "done" >>apache-airflow-providers-ftp-feedstock.mark ) && true) || ( (echo "apache-airflow-providers-ftp-feedstock" >>failed.23 ) && (echo "apache-airflow-providers-ftp-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "apache-airflow-providers-ftp-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f apache-airflow-providers-http-feedstock.mark ]]; then
    if [[ -d apache-airflow-providers-http-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./apache-airflow-providers-http-feedstock >d 2>&1 && rm -f d && ( echo "done" >>apache-airflow-providers-http-feedstock.mark ) && true) || ( (echo "apache-airflow-providers-http-feedstock" >>failed.23 ) && (echo "apache-airflow-providers-http-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "apache-airflow-providers-http-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f apache-airflow-providers-imap-feedstock.mark ]]; then
    if [[ -d apache-airflow-providers-imap-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./apache-airflow-providers-imap-feedstock >d 2>&1 && rm -f d && ( echo "done" >>apache-airflow-providers-imap-feedstock.mark ) && true) || ( (echo "apache-airflow-providers-imap-feedstock" >>failed.23 ) && (echo "apache-airflow-providers-imap-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "apache-airflow-providers-imap-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f apache-airflow-providers-sqlite-feedstock.mark ]]; then
    if [[ -d apache-airflow-providers-sqlite-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./apache-airflow-providers-sqlite-feedstock >d 2>&1 && rm -f d && ( echo "done" >>apache-airflow-providers-sqlite-feedstock.mark ) && true) || ( (echo "apache-airflow-providers-sqlite-feedstock" >>failed.23 ) && (echo "apache-airflow-providers-sqlite-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "apache-airflow-providers-sqlite-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f arrow-cpp-feedstock.mark ]]; then
    if [[ -d arrow-cpp-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./arrow-cpp-feedstock >d 2>&1 && rm -f d && ( echo "done" >>arrow-cpp-feedstock.mark ) && true) || ( (echo "arrow-cpp-feedstock" >>failed.23 ) && (echo "arrow-cpp-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "arrow-cpp-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f astroid-feedstock.mark ]]; then
    if [[ -d astroid-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./astroid-feedstock >d 2>&1 && rm -f d && ( echo "done" >>astroid-feedstock.mark ) && true) || ( (echo "astroid-feedstock" >>failed.23 ) && (echo "astroid-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "astroid-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f blinker-feedstock.mark ]]; then
    if [[ -d blinker-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./blinker-feedstock/ >d 2>&1 && rm -f d && ( echo "done" >>blinker-feedstock.mark ) && true) || ( (echo "blinker-feedstock" >>failed.23 ) && (echo "blinker-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "blinker-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f bokeh-feedstock.mark ]]; then
    if [[ -d bokeh-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./bokeh-feedstock >d 2>&1 && rm -f d && ( echo "done" >>bokeh-feedstock.mark ) && true) || ( (echo "bokeh-feedstock" >>failed.23 ) && (echo "bokeh-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "bokeh-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f bokeh-2.4.3-feedstock.mark ]]; then
    if [[ -d bokeh-2.4.3-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./bokeh-2.4.3-feedstock >d 2>&1 && rm -f d && ( echo "done" >>bokeh-2.4.3-feedstock.mark ) && true) || ( (echo "bokeh-2.4.3-feedstock" >>failed.23 ) && (echo "bokeh-2.4.3-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "bokeh-2.4.3-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f boto3-feedstock.mark ]]; then
    if [[ -d boto3-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./boto3-feedstock >d 2>&1 && rm -f d && ( echo "done" >>boto3-feedstock.mark ) && true) || ( (echo "boto3-feedstock" >>failed.23 ) && (echo "boto3-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "boto3-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f catalogue-feedstock.mark ]]; then
    if [[ -d catalogue-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./catalogue-feedstock >d 2>&1 && rm -f d && ( echo "done" >>catalogue-feedstock.mark ) && true) || ( (echo "catalogue-feedstock" >>failed.23 ) && (echo "catalogue-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "catalogue-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f cattrs-feedstock.mark ]]; then
    if [[ -d cattrs-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./cattrs-feedstock >d 2>&1 && rm -f d && ( echo "done" >>cattrs-feedstock.mark ) && true) || ( (echo "cattrs-feedstock" >>failed.23 ) && (echo "cattrs-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "cattrs-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f cftime-feedstock.mark ]]; then
    if [[ -d cftime-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./cftime-feedstock >d 2>&1 && rm -f d && ( echo "done" >>cftime-feedstock.mark ) && true) || ( (echo "cftime-feedstock" >>failed.23 ) && (echo "cftime-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "cftime-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f chardet-feedstock.mark ]]; then
    if [[ -d chardet-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./chardet-feedstock >d 2>&1 && rm -f d && ( echo "done" >>chardet-feedstock.mark ) && true) || ( (echo "chardet-feedstock" >>failed.23 ) && (echo "chardet-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "chardet-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f colorlog-feedstock.mark ]]; then
    if [[ -d colorlog-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./colorlog-feedstock >d 2>&1 && rm -f d && ( echo "done" >>colorlog-feedstock.mark ) && true) || ( (echo "colorlog-feedstock" >>failed.23 ) && (echo "colorlog-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "colorlog-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f conda-package-handling-feedstock.mark ]]; then
    if [[ -d conda-package-handling-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./conda-package-handling-feedstock >d 2>&1 && rm -f d && ( echo "done" >>conda-package-handling-feedstock.mark ) && true) || ( (echo "conda-package-handling-feedstock" >>failed.23 ) && (echo "conda-package-handling-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "conda-package-handling-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f configupdater-feedstock.mark ]]; then
    if [[ -d configupdater-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./configupdater-feedstock >d 2>&1 && rm -f d && ( echo "done" >>configupdater-feedstock.mark ) && true) || ( (echo "configupdater-feedstock" >>failed.23 ) && (echo "configupdater-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "configupdater-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f connexion-feedstock.mark ]]; then
    if [[ -d connexion-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./connexion-feedstock >d 2>&1 && rm -f d && ( echo "done" >>connexion-feedstock.mark ) && true) || ( (echo "connexion-feedstock" >>failed.23 ) && (echo "connexion-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "connexion-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f cron-descriptor-feedstock.mark ]]; then
    if [[ -d cron-descriptor-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./cron-descriptor-feedstock >d 2>&1 && rm -f d && ( echo "done" >>cron-descriptor-feedstock.mark ) && true) || ( (echo "cron-descriptor-feedstock" >>failed.23 ) && (echo "cron-descriptor-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "cron-descriptor-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f croniter-feedstock.mark ]]; then
    if [[ -d croniter-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./croniter-feedstock >d 2>&1 && rm -f d && ( echo "done" >>croniter-feedstock.mark ) && true) || ( (echo "croniter-feedstock" >>failed.23 ) && (echo "croniter-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "croniter-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f cymem-feedstock.mark ]]; then
    if [[ -d cymem-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./cymem-feedstock >d 2>&1 && rm -f d && ( echo "done" >>cymem-feedstock.mark ) && true) || ( (echo "cymem-feedstock" >>failed.23 ) && (echo "cymem-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "cymem-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f dask-core-feedstock.mark ]]; then
    if [[ -d dask-core-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./dask-core-feedstock >d 2>&1 && rm -f d && ( echo "done" >>dask-core-feedstock.mark ) && true) || ( (echo "dask-core-feedstock" >>failed.23 ) && (echo "dask-core-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "dask-core-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f deprecated-feedstock.mark ]]; then
    if [[ -d deprecated-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./deprecated-feedstock >d 2>&1 && rm -f d && ( echo "done" >>deprecated-feedstock.mark ) && true) || ( (echo "deprecated-feedstock" >>failed.23 ) && (echo "deprecated-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "deprecated-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f dill-feedstock.mark ]]; then
    if [[ -d dill-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./dill-feedstock >d 2>&1 && rm -f d && ( echo "done" >>dill-feedstock.mark ) && true) || ( (echo "dill-feedstock" >>failed.23 ) && (echo "dill-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "dill-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f et_xmlfile-feedstock.mark ]]; then
    if [[ -d et_xmlfile-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./et_xmlfile-feedstock >d 2>&1 && rm -f d && ( echo "done" >>et_xmlfile-feedstock.mark ) && true) || ( (echo "et_xmlfile-feedstock" >>failed.23 ) && (echo "et_xmlfile-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "et_xmlfile-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f flask-appbuilder-feedstock.mark ]]; then
    if [[ -d flask-appbuilder-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./flask-appbuilder-feedstock >d 2>&1 && rm -f d && ( echo "done" >>flask-appbuilder-feedstock.mark ) && true) || ( (echo "flask-appbuilder-feedstock" >>failed.23 ) && (echo "flask-appbuilder-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "flask-appbuilder-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f flask-caching-feedstock.mark ]]; then
    if [[ -d flask-caching-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./flask-caching-feedstock >d 2>&1 && rm -f d && ( echo "done" >>flask-caching-feedstock.mark ) && true) || ( (echo "flask-caching-feedstock" >>failed.23 ) && (echo "flask-caching-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "flask-caching-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f flask-session-feedstock.mark ]]; then
    if [[ -d flask-session-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./flask-session-feedstock >d 2>&1 && rm -f d && ( echo "done" >>flask-session-feedstock.mark ) && true) || ( (echo "flask-session-feedstock" >>failed.23 ) && (echo "flask-session-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "flask-session-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f gitpython-feedstock.mark ]]; then
    if [[ -d gitpython-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./gitpython-feedstock >d 2>&1 && rm -f d && ( echo "done" >>gitpython-feedstock.mark ) && true) || ( (echo "gitpython-feedstock" >>failed.23 ) && (echo "gitpython-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "gitpython-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f googleapis-common-protos-feedstock.mark ]]; then
    if [[ -d googleapis-common-protos-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./googleapis-common-protos-feedstock >d 2>&1 && rm -f d && ( echo "done" >>googleapis-common-protos-feedstock.mark ) && true) || ( (echo "googleapis-common-protos-feedstock" >>failed.23 ) && (echo "googleapis-common-protos-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "googleapis-common-protos-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f grpcio-feedstock.mark ]]; then
    if [[ -d grpcio-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./grpcio-feedstock >d 2>&1 && rm -f d && ( echo "done" >>grpcio-feedstock.mark ) && true) || ( (echo "grpcio-feedstock" >>failed.23 ) && (echo "grpcio-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "grpcio-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f gunicorn-feedstock.mark ]]; then
    if [[ -d gunicorn-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./gunicorn-feedstock >d 2>&1 && rm -f d && ( echo "done" >>gunicorn-feedstock.mark ) && true) || ( (echo "gunicorn-feedstock" >>failed.23 ) && (echo "gunicorn-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "gunicorn-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f httpx-feedstock.mark ]]; then
    if [[ -d httpx-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./httpx-feedstock >d 2>&1 && rm -f d && ( echo "done" >>httpx-feedstock.mark ) && true) || ( (echo "httpx-feedstock" >>failed.23 ) && (echo "httpx-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "httpx-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f joblib-feedstock.mark ]]; then
    if [[ -d joblib-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./joblib-feedstock >d 2>&1 && rm -f d && ( echo "done" >>joblib-feedstock.mark ) && true) || ( (echo "joblib-feedstock" >>failed.23 ) && (echo "joblib-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "joblib-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f jupyter_console-feedstock.mark ]]; then
    if [[ -d jupyter_console-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./jupyter_console-feedstock >d 2>&1 && rm -f d && ( echo "done" >>jupyter_console-feedstock.mark ) && true) || ( (echo "jupyter_console-feedstock" >>failed.23 ) && (echo "jupyter_console-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "jupyter_console-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f kiwisolver-feedstock.mark ]]; then
    if [[ -d kiwisolver-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./kiwisolver-feedstock >d 2>&1 && rm -f d && ( echo "done" >>kiwisolver-feedstock.mark ) && true) || ( (echo "kiwisolver-feedstock" >>failed.23 ) && (echo "kiwisolver-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "kiwisolver-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f leather-feedstock.mark ]]; then
    if [[ -d leather-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./leather-feedstock >d 2>&1 && rm -f d && ( echo "done" >>leather-feedstock.mark ) && true) || ( (echo "leather-feedstock" >>failed.23 ) && (echo "leather-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "leather-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f linkify-it-py-feedstock.mark ]]; then
    if [[ -d linkify-it-py-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./linkify-it-py-feedstock >d 2>&1 && rm -f d && ( echo "done" >>linkify-it-py-feedstock.mark ) && true) || ( (echo "linkify-it-py-feedstock" >>failed.23 ) && (echo "linkify-it-py-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "linkify-it-py-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f markdown-feedstock.mark ]]; then
    if [[ -d markdown-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./markdown-feedstock >d 2>&1 && rm -f d && ( echo "done" >>markdown-feedstock.mark ) && true) || ( (echo "markdown-feedstock" >>failed.23 ) && (echo "markdown-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "markdown-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f marshmallow-oneofschema-feedstock.mark ]]; then
    if [[ -d marshmallow-oneofschema-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./marshmallow-oneofschema-feedstock >d 2>&1 && rm -f d && ( echo "done" >>marshmallow-oneofschema-feedstock.mark ) && true) || ( (echo "marshmallow-oneofschema-feedstock" >>failed.23 ) && (echo "marshmallow-oneofschema-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "marshmallow-oneofschema-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f mdit-py-plugins-feedstock.mark ]]; then
    if [[ -d mdit-py-plugins-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./mdit-py-plugins-feedstock >d 2>&1 && rm -f d && ( echo "done" >>mdit-py-plugins-feedstock.mark ) && true) || ( (echo "mdit-py-plugins-feedstock" >>failed.23 ) && (echo "mdit-py-plugins-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "mdit-py-plugins-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f murmurhash-feedstock.mark ]]; then
    if [[ -d murmurhash-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./murmurhash-feedstock >d 2>&1 && rm -f d && ( echo "done" >>murmurhash-feedstock.mark ) && true) || ( (echo "murmurhash-feedstock" >>failed.23 ) && (echo "murmurhash-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "murmurhash-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f mypy_extensions-feedstock.mark ]]; then
    if [[ -d mypy_extensions-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./mypy_extensions-feedstock >d 2>&1 && rm -f d && ( echo "done" >>mypy_extensions-feedstock.mark ) && true) || ( (echo "mypy_extensions-feedstock" >>failed.23 ) && (echo "mypy_extensions-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "mypy_extensions-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f onnx-feedstock.mark ]]; then
    if [[ -d onnx-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./onnx-feedstock >d 2>&1 && rm -f d && ( echo "done" >>onnx-feedstock.mark ) && true) || ( (echo "onnx-feedstock" >>failed.23 ) && (echo "onnx-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "onnx-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f opencv-feedstock.mark ]]; then
    if [[ -d opencv-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./opencv-feedstock >d 2>&1 && rm -f d && ( echo "done" >>opencv-feedstock.mark ) && true) || ( (echo "opencv-feedstock" >>failed.23 ) && (echo "opencv-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "opencv-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f parsedatetime-feedstock.mark ]]; then
    if [[ -d parsedatetime-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./parsedatetime-feedstock >d 2>&1 && rm -f d && ( echo "done" >>parsedatetime-feedstock.mark ) && true) || ( (echo "parsedatetime-feedstock" >>failed.23 ) && (echo "parsedatetime-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "parsedatetime-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f pycosat-feedstock.mark ]]; then
    if [[ -d pycosat-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./pycosat-feedstock >d 2>&1 && rm -f d && ( echo "done" >>pycosat-feedstock.mark ) && true) || ( (echo "pycosat-feedstock" >>failed.23 ) && (echo "pycosat-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "pycosat-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f pyct-feedstock.mark ]]; then
    if [[ -d pyct-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./pyct-feedstock >d 2>&1 && rm -f d && ( echo "done" >>pyct-feedstock.mark ) && true) || ( (echo "pyct-feedstock" >>failed.23 ) && (echo "pyct-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "pyct-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f pyinstaller-hooks-contrib-feedstock.mark ]]; then
    if [[ -d pyinstaller-hooks-contrib-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./pyinstaller-hooks-contrib-feedstock >d 2>&1 && rm -f d && ( echo "done" >>pyinstaller-hooks-contrib-feedstock.mark ) && true) || ( (echo "pyinstaller-hooks-contrib-feedstock" >>failed.23 ) && (echo "pyinstaller-hooks-contrib-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "pyinstaller-hooks-contrib-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f pykerberos-feedstock.mark ]]; then
    if [[ -d pykerberos-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./pykerberos-feedstock >d 2>&1 && rm -f d && ( echo "done" >>pykerberos-feedstock.mark ) && true) || ( (echo "pykerberos-feedstock" >>failed.23 ) && (echo "pykerberos-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "pykerberos-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f python-daemon-feedstock.mark ]]; then
    if [[ -d python-daemon-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./python-daemon-feedstock >d 2>&1 && rm -f d && ( echo "done" >>python-daemon-feedstock.mark ) && true) || ( (echo "python-daemon-feedstock" >>failed.23 ) && (echo "python-daemon-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "python-daemon-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f python-graphviz-feedstock.mark ]]; then
    if [[ -d python-graphviz-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./python-graphviz-feedstock >d 2>&1 && rm -f d && ( echo "done" >>python-graphviz-feedstock.mark ) && true) || ( (echo "python-graphviz-feedstock" >>failed.23 ) && (echo "python-graphviz-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "python-graphviz-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f pytimeparse-feedstock.mark ]]; then
    if [[ -d pytimeparse-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./pytimeparse-feedstock >d 2>&1 && rm -f d && ( echo "done" >>pytimeparse-feedstock.mark ) && true) || ( (echo "pytimeparse-feedstock" >>failed.23 ) && (echo "pytimeparse-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "pytimeparse-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f rich-feedstock.mark ]]; then
    if [[ -d rich-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./rich-feedstock >d 2>&1 && rm -f d && ( echo "done" >>rich-feedstock.mark ) && true) || ( (echo "rich-feedstock" >>failed.23 ) && (echo "rich-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "rich-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f ruamel.yaml-feedstock.mark ]]; then
    if [[ -d ruamel.yaml-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./ruamel.yaml-feedstock >d 2>&1 && rm -f d && ( echo "done" >>ruamel.yaml-feedstock.mark ) && true) || ( (echo "ruamel.yaml-feedstock" >>failed.23 ) && (echo "ruamel.yaml-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "ruamel.yaml-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f scipy-feedstock.mark ]]; then
    if [[ -d scipy-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./scipy-feedstock >d 2>&1 && rm -f d && ( echo "done" >>scipy-feedstock.mark ) && true) || ( (echo "scipy-feedstock" >>failed.23 ) && (echo "scipy-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "scipy-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f setproctitle-feedstock.mark ]]; then
    if [[ -d setproctitle-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./setproctitle-feedstock >d 2>&1 && rm -f d && ( echo "done" >>setproctitle-feedstock.mark ) && true) || ( (echo "setproctitle-feedstock" >>failed.23 ) && (echo "setproctitle-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "setproctitle-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f setuptools_scm_git_archive-feedstock.mark ]]; then
    if [[ -d setuptools_scm_git_archive-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./setuptools_scm_git_archive-feedstock >d 2>&1 && rm -f d && ( echo "done" >>setuptools_scm_git_archive-feedstock.mark ) && true) || ( (echo "setuptools_scm_git_archive-feedstock" >>failed.23 ) && (echo "setuptools_scm_git_archive-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "setuptools_scm_git_archive-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f swagger-ui-bundle-feedstock.mark ]]; then
    if [[ -d swagger-ui-bundle-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./swagger-ui-bundle-feedstock >d 2>&1 && rm -f d && ( echo "done" >>swagger-ui-bundle-feedstock.mark ) && true) || ( (echo "swagger-ui-bundle-feedstock" >>failed.23 ) && (echo "swagger-ui-bundle-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "swagger-ui-bundle-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f tabulate-feedstock.mark ]]; then
    if [[ -d tabulate-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./tabulate-feedstock >d 2>&1 && rm -f d && ( echo "done" >>tabulate-feedstock.mark ) && true) || ( (echo "tabulate-feedstock" >>failed.23 ) && (echo "tabulate-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "tabulate-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f tenacity-feedstock.mark ]]; then
    if [[ -d tenacity-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./tenacity-feedstock >d 2>&1 && rm -f d && ( echo "done" >>tenacity-feedstock.mark ) && true) || ( (echo "tenacity-feedstock" >>failed.23 ) && (echo "tenacity-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "tenacity-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f termcolor-feedstock.mark ]]; then
    if [[ -d termcolor-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./termcolor-feedstock >d 2>&1 && rm -f d && ( echo "done" >>termcolor-feedstock.mark ) && true) || ( (echo "termcolor-feedstock" >>failed.23 ) && (echo "termcolor-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "termcolor-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f ujson-feedstock.mark ]]; then
    if [[ -d ujson-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./ujson-feedstock >d 2>&1 && rm -f d && ( echo "done" >>ujson-feedstock.mark ) && true) || ( (echo "ujson-feedstock" >>failed.23 ) && (echo "ujson-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "ujson-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f unicodecsv-feedstock.mark ]]; then
    if [[ -d unicodecsv-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./unicodecsv-feedstock >d 2>&1 && rm -f d && ( echo "done" >>unicodecsv-feedstock.mark ) && true) || ( (echo "unicodecsv-feedstock" >>failed.23 ) && (echo "unicodecsv-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "unicodecsv-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f waf-feedstock.mark ]]; then
    if [[ -d waf-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./waf-feedstock >d 2>&1 && rm -f d && ( echo "done" >>waf-feedstock.mark ) && true) || ( (echo "waf-feedstock" >>failed.23 ) && (echo "waf-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "waf-feedstock not present" >>failed.23
    fi
fi


if [[ ! -f zict-feedstock.mark ]]; then
    if [[ -d zict-feedstock ]]; then
        (conda-build --python=3.11 --numpy=1.22 --croot=../ci_py311/ -c py311_bs/label/release --use-local --no-test ./zict-feedstock >d 2>&1 && rm -f d && ( echo "done" >>zict-feedstock.mark ) && true) || ( (echo "zict-feedstock" >>failed.23 ) && (echo "zict-feedstock" >>errors.dump ) && ( cat d >>errors.dump ) && cat d && rm -f d && true) || true
    else
        echo "zict-feedstock not present" >>failed.23
    fi
fi

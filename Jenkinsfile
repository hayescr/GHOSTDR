#!/usr/bin/env groovy
/*
 * Jenkins Pipeline for GHOSTDR
 *
 * by Chris Simpson (adapted from BCQ's DRAGONS pipeline)
 *
 * Required Plug-ins:
 * - CloudBees File Leak Detector?
 * - Cobertura Plug-in?
 * - Warnings NG?
 */

pipeline {

    agent any

    options {
        skipDefaultCheckout(true)
        buildDiscarder(logRotator(numToKeepStr: '5'))
        timestamps()
        timeout(time: 4, unit: 'HOURS')
    }

    stages {

        /*
        stage ("Unit tests") {
            environment {
                MPLBACKEND = "agg"
                PATH = "$JENKINS_CONDA_HOME/bin:$PATH"
                DRAGONS_TEST_OUT = "./unit_tests_outputs/"
                TOX_ARGS = "ghost_instruments ghostdr"
                TMPDIR = "${env.WORKSPACE}/.tmp/unit/"
            }
            steps {
                echo "Running build #${env.BUILD_ID} on ${env.NODE_NAME}"
                checkout scm
                echo "${env.PATH}"
                sh '.jenkins/scripts/setup_agent.sh'
                sh 'tox -e ghost-unit -v -r -- --basetemp=${DRAGONS_TEST_OUT} ${TOX_ARGS}'
            }
        }

        stage ("Bundle tests") {
            environment {
                MPLBACKEND = "agg"
                PATH = "$JENKINS_CONDA_HOME/bin:$PATH"
                DRAGONS_TEST_OUT = "./bundle_tests_outputs/"
                TOX_ARGS = "ghost_instruments ghostdr"
                TMPDIR = "${env.WORKSPACE}/.tmp/bundle/"
            }
            steps {
                echo "Running build #${env.BUILD_ID} on ${env.NODE_NAME}"
                checkout scm
                echo "${env.PATH}"
                sh '.jenkins/scripts/setup_agent.sh'
                sh 'tox -e ghost-ghostbundle -v -r -- --basetemp=${DRAGONS_TEST_OUT} ${TOX_ARGS}'
            }

        }
        */

        stage ("SLITV tests") {
            environment {
                MPLBACKEND = "agg"
                PATH = "$JENKINS_CONDA_HOME/bin:$PATH"
                DRAGONS_TEST_OUT = "./slit_tests_outputs/"
                TOX_ARGS = "ghost_instruments ghostdr"
                TMPDIR = "${env.WORKSPACE}/.tmp/slit/"
            }
            steps {
                echo "Running build #${env.BUILD_ID} on ${env.NODE_NAME}"
                checkout scm
                echo "${env.PATH}"
                sh '.jenkins/scripts/setup_agent.sh'
                sh 'tox -e ghost-ghostslit -v -r -- --basetemp=${DRAGONS_TEST_OUT} ${TOX_ARGS}'
            }

        }


    }

    post {
        success {
            deleteDir() /* clean up our workspace */
        }
        failure {
            deleteDir()
        }
    }


}
#!/usr/bin/env python3

import urllib.request
import unittest
import os


def download_files(cwd):

    url = [
        "https://raw.githubusercontent.com/apache/thrift/43f4bf2fdd13c7466e3fea690d436c6a9540f303/lib/c_glib/test/testbinaryprotocol.c",
        "https://raw.githubusercontent.com/apache/thrift/43f4bf2fdd13c7466e3fea690d436c6a9540f303/lib/cpp/test/AnnotationTest.cpp",
        "https://raw.githubusercontent.com/apache/thrift/43f4bf2fdd13c7466e3fea690d436c6a9540f303/lib/go/test/tests/thrifttest_driver.go",
        "https://raw.githubusercontent.com/apache/thrift/43f4bf2fdd13c7466e3fea690d436c6a9540f303/lib/hs/test/JSONSpec.hs",
        "https://raw.githubusercontent.com/necolas/normalize.css/fc091cce1534909334c1911709a39c22d406977b/normalize.css",
        "https://raw.githubusercontent.com/apache/thrift/43f4bf2fdd13c7466e3fea690d436c6a9540f303/lib/java/test/org/apache/thrift/test/JavaBeansTest.java",
        "https://raw.githubusercontent.com/apache/thrift/43f4bf2fdd13c7466e3fea690d436c6a9540f303/lib/js/test/test-async.js",
        "https://raw.githubusercontent.com/apache/thrift/8101f00b0966deebd36a6ba658aa59d718453345/lib/perl/tools/FixupDist.pl",
        "https://raw.githubusercontent.com/apache/thrift/9ea48f362a578ee8556fcf3ca84215cefbc1b99e/lib/php/test/Fixtures.php",
        "https://raw.githubusercontent.com/apache/thrift/43f4bf2fdd13c7466e3fea690d436c6a9540f303/lib/py/test/test_sslsocket.py",
        "https://raw.githubusercontent.com/apache/thrift/43f4bf2fdd13c7466e3fea690d436c6a9540f303/lib/rb/benchmark/benchmark.rb",
        "https://raw.githubusercontent.com/apache/thrift/43f4bf2fdd13c7466e3fea690d436c6a9540f303/lib/rs/test/src/bin/kitchen_sink_client.rs",
        "https://raw.githubusercontent.com/apache/thrift/a082592d439d6aa578507ff52198038e5e08006d/lib/swift/Tests/ThriftTests/TFramedTransportTests.swift",
        "https://raw.githubusercontent.com/deanwampler/programming-scala-book-code-examples/3792ec69b22538be7864b0880ee8f36ae6f97867/src/main/scala-2/progscala3/meta/Func.scala",
        "https://raw.githubusercontent.com/janosgyerik/shellscripts/2bf11a0b5c061b913aba6c3b161daf1c1bdb4536/bash/find-recent.sh",
        "https://raw.githubusercontent.com/antoniolg/Bandhook-Kotlin/5caffc8eaefcbb2d5c0e4bcd1590c306755208a8/app/build.gradle.kts",
        "https://raw.githubusercontent.com/avouros/toolset/6d044ad52777be48b8a5f56c79b81b733ac46c92/scripts/BarPlotErrorbars.m",
        "https://raw.githubusercontent.com/r-lib/rlang/6dbcae3fc9af9e75b27053b28e7ae81e0717a387/R/arg.R",
        "https://raw.githubusercontent.com/ttu/csharp-tutorial/5e5f94334a8f1111ae03ef0e2d109721da6757e9/csharp-tutorial/13_Parallel.cs",
        "https://raw.githubusercontent.com/cfjedimaster/HTML-Code-Demos/89090b8b19d666e4552846a6ea27f42813c0877e/code/forms/10_validation.html",
        "https://raw.githubusercontent.com/apache/thrift/f86845e8ed622e7e3b7c87f00f16729ee6cc524d/lib/ts/test/phantom-client.ts",
        "https://raw.githubusercontent.com/airbnb/react-with-styles/2532394bb866aaade4dc750ee94c0ff213d9b6de/src/withStyles.jsx",
        "https://raw.githubusercontent.com/flutter/plugins/e61e9d45bcaadc3e409d529d30735cb4db75c5c5/packages/android_alarm_manager/lib/android_alarm_manager.dart",
        "https://raw.githubusercontent.com/microsoft/TypeScript/c33a14d66d0a452673ce77256e178bf84e875d2b/tests/cases/user/formik/index.tsx" 
    ]

    directory = os.path.join(cwd, "nirjas/languages/tests/TestFiles")

    if not os.path.isdir(directory):
        print("Downloading test files")
        os.mkdir(directory)
        for i in url:
            list_of = i.split(".")
            ext = [list_of[-1]]
            data = urllib.request.urlopen(i)

            for j in range (len(ext)):
                filename = "textcomment." + ext[j]
                f = open(os.path.join(directory,filename),'w')
                f.write(data.read().decode('utf-8'))
                f.close
                print(".", end="")
        print()

if __name__ == "__main__":
    here = os.path.abspath(os.path.dirname(__file__))
    download_files(here)
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover('nirjas/languages/tests',
                                      pattern='test_*.py')
    result = test_runner.run(test_suite)
    exit(int(not result.wasSuccessful()))

set JUNIT_HOME=C:\opt\lib
set CLASSPATH=%CLASSPATH%;%JUNIT_HOME%\hamcrest-core-1.3.jar;%JUNIT_HOME%\junit-4.12.jar;.;
javac src\MathGame9x9.java src\MyConsole.java src\TestMathGame9x9.java src\TestRunner.java -d out\production\game_9x9_java\
cd out\production\game_9x9_java && java MyConsole && cd ..\..\..
cd out\production\game_9x9_java && java TestRunner && cd ..\..\..

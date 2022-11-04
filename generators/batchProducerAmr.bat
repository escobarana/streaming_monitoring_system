@ECHO OFF
ECHO.
ECHO.
ECHO ---------- Batch to produce  sensors data to  kafka topic will start ( takes approximately 5 to 10 minutes to complete ) ----------
ECHO.
ECHO.
ECHO Producing 5 pushes to the kafka topic containing subsets of records:
ECHO.
ECHO.


for /L %%n in (1,1,5) do call :producer_function %%n
ECHO.
ECHO.
ECHO ********* 5 pushes produced successfully *********
ECHO.
ECHO.
ECHO.
ECHO.
ECHO.


EXIT /B %ERRORLEVEL%

:producer_function
ECHO.
ECHO Push Number %~1
ECHO.
python amr.py
EXIT /B 0


PAUSE

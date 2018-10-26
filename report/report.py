#!/usr/bin/python3.5

import MySQLdb
import os, sys
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import urllib.request
import time
from shutil import copyfile

# Initial First File Opening
first = True

def getmsg():

    # Connection to semaphore mysql database
    db = MySQLdb.connect("localhost","root","******","semaphore" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Query for completed playbooks
    sql1 = "SELECT task_id,output FROM task__output WHERE output like '%Playbook Completed%'"
    try:
        # Execute the SQL command
        cursor.execute(sql1)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        try:
            for row in results:
            # Now print fetched result
                msg = row[1]
                result=msg.split("#")
                Task_ID=row[0]
                TTP_ID=result[1]
                status=result[2]
                os=result[3]
                try:
                    # Query to grave task completion date
                    sql2 = "SELECT end FROM task WHERE id=%d" % (Task_ID)
                    cursor.execute(sql2)
                    task_result = cursor.fetchall()
                    for row in task_result:
                        date=row[0]
                except:
                    print ("Failed to query date")
                updatereport(TTP_ID,status,date,os)
        except:
            print("Failed to query task")
    except:
        print ("Error: unable to fecth data")

    # disconnect from server
    db.close()

def updatereport(TTP_ID,status,date,os):
    # Load in the workbook
    global first
    # Load matrix template
    if (first == True):
        try:
            url= "https://github.com/rallyspeed/ansible-mitre/raw/master/report/Matrix-MITRE.xlsx"
            urllib.request.urlretrieve(url, "Updated-Matrix.xlsx")
            wb = load_workbook('./Updated-Matrix.xlsx')
            first = False
        except:
            print ("Failed to donwlod URL")

    # Load updated matrix
    else:
        wb = load_workbook('/var/www/html/matrix.xlsx')
    if (os == "win"):
        ws = wb['windows']
    elif (os == "linux"):
        ws = wb['linux']
    # ws = wb.active  # Use default/active sheet
    r = int(ws.max_row)
    c = int(ws.max_column)
    try:
        for i in range(1, r+1):
            for j in range(1, c+1):
                cv = ws.cell(row=i, column=j).value
                if TTP_ID == cv:
                # Change color of TTP cell which playbook was run succesfully and add date
                    ws.cell(row=i,column=j).fill = PatternFill(start_color="8470FF", end_color="8470FF",fill_type = "solid")
                    ws.cell(row=i,column=j+1).fill = PatternFill(start_color="8470FF", end_color="8470FF",fill_type = "solid")
                    ws.cell(row=i,column=j+1).value = date
                # Green color 00FF00 if TTP blocked
                    if status == "blocked":
                        ws.cell(row=i,column=j-1).fill = PatternFill(start_color="00FF00", end_color="FF0000",fill_type = "solid")
                # Red color FF0000 if TTP not blocked
                    elif status == "passed":
                        ws.cell(row=i,column=j-1).fill = PatternFill(start_color="FF0000", end_color="00FF00",fill_type = "solid")
                 # Orange color FFA500 if TTP failed
                    elif status == "failed":
                        ws.cell(row=i,column=j-1).fill = PatternFill(start_color="FFA500", end_color="00FF00",fill_type = "solid")
    except:
        print ("failed to loop through xls")
    wb.save("/var/www/html/matrix.xlsx")

def savereport():
    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M', t)
    copyfile("/var/www/html/matrix.xlsx","/var/www/html/matrix" + timestamp + ".xlsx")
    print("File available: http://35.210.224.241/matrix" + timestamp + ".xlsx")

def main():
    getmsg()
    savereport()

if __name__ == '__main__':
    main()

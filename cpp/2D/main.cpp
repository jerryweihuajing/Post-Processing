﻿// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title: Script-main
******************************************************************************/

#include <iostream>
#include <string>
#include <fstream>

using namespace std;

int main()
{
	cout << "Welcome to YADEM!" << endl;

	string path_input_file;

	//ofstream input_file;
	//input_file.open(path_input_file);

    int no_os_flag = 1;

#ifdef linux

    no_os_flag = 0;

    cout << "It is in Linux OS!" << endl;

#endif

#ifdef _WIN64

    no_os_flag = 0;

    cout << "It is in Windows OS!" << endl;

#endif

    if (1 == no_os_flag) {

        cout << "No OS Defined ,I do not know what the os is!" << endl;

    }

    return 0;
}

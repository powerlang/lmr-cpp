/*
 * Copyright (c) 2020 Javier Pimas & LabWare
 *
 * This program and the accompanying materials are made available under
 * the terms of the MIT license, see LICENSE file.
 *
 * SPDX-License-Identifier: MIT
 */

#ifndef LAUNCHER_LAUNCHER_H_
#define LAUNCHER_LAUNCHER_H_

#include <fstream>

#include "ImageSegment.h"

class Launcher
{
public:
	int main(const int argc, const char** argv);

protected:

    int launch(ImageSegment *kernel, const int argc, const char **argv);
};

#endif /* LAUNCHER_LAUNCHER_H_ */


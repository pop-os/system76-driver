/*******************************************************************************
#	 	spcadecoder: Generic decoder for various input stream yyuv	#
# yuyv yuvy jpeg411 jpeg422 bayer rggb with gamma correct			#
# and various output palette rgb16 rgb24 rgb32 yuv420p				#
# various output size with crop feature						#
# 		Copyright (C) 2003 2004 2005 Michel Xhaard			#
# 		mxhaard@magic.fr						#
# 		Sonix Decompressor by Bertrik.Sikken. (C) 2004			#
# 		Pixart Decompressor by Bertrik.Sikken. Thomas Kaiser (C) 2005	#
# 		Spca561decoder (C) 2005 Andrzej Szombierski [qq@kuku.eu.org]	#
# This program is free software; you can redistribute it and/or modify		#
# it under the terms of the GNU General Public License as published by		#
# the Free Software Foundation; either version 2 of the License, or		#
# (at your option) any later version.						#
#										#
# This program is distributed in the hope that it will be useful,		#
# but WITHOUT ANY WARRANTY; without even the implied warranty of		#
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the			#
# GNU General Public License for more details.					#
#										#
# You should have received a copy of the GNU General Public License		#
# along with this program; if not, write to the Free Software			#
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA	#
********************************************************************************/


#ifndef __KERNEL__
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#else				/* __KERNEL__ */
#include <linux/string.h>
#endif				/* __KERNEL__ */


#include "gspcadecoder.h"
#include "../utils/spcagamma.h"

#define ISHIFT 11

#define IFIX(a) ((long)((a) * (1 << ISHIFT) + .5))
#define IMULT(a, b) (((a) * (b)) >> ISHIFT)
#define ITOINT(a) ((a) >> ISHIFT)

/* special markers */
#define M_BADHUFF	-1


#define ERR_NO_SOI 1
#define ERR_NOT_8BIT 2
#define ERR_HEIGHT_MISMATCH 3
#define ERR_WIDTH_MISMATCH 4
#define ERR_BAD_WIDTH_OR_HEIGHT 5
#define ERR_TOO_MANY_COMPPS 6
#define ERR_ILLEGAL_HV 7
#define ERR_QUANT_TABLE_SELECTOR 8
#define ERR_NOT_YCBCR_221111 9
#define ERR_UNKNOWN_CID_IN_SCAN 10
#define ERR_NOT_SEQUENTIAL_DCT 11
#define ERR_WRONG_MARKER 12
#define ERR_NO_EOI 13
#define ERR_BAD_TABLES 14
#define ERR_DEPTH_MISMATCH 15
#define ERR_CORRUPTFRAME 16

#define JPEGHEADER_LENGTH 589

const unsigned char JPEGHeader[JPEGHEADER_LENGTH] = {
    0xff, 0xd8, 0xff, 0xdb, 0x00, 0x84, 0x00, 0x06, 0x04, 0x05, 0x06,
    0x05, 0x04, 0x06, 0x06, 0x05,
    0x06, 0x07, 0x07, 0x06, 0x08, 0x0a, 0x10, 0x0a, 0x0a, 0x09, 0x09,
    0x0a, 0x14, 0x0e, 0x0f, 0x0c,
    0x10, 0x17, 0x14, 0x18, 0x18, 0x17, 0x14, 0x16, 0x16, 0x1a, 0x1d,
    0x25, 0x1f, 0x1a, 0x1b, 0x23,
    0x1c, 0x16, 0x16, 0x20, 0x2c, 0x20, 0x23, 0x26, 0x27, 0x29, 0x2a,
    0x29, 0x19, 0x1f, 0x2d, 0x30,
    0x2d, 0x28, 0x30, 0x25, 0x28, 0x29, 0x28, 0x01, 0x07, 0x07, 0x07,
    0x0a, 0x08, 0x0a, 0x13, 0x0a,
    0x0a, 0x13, 0x28, 0x1a, 0x16, 0x1a, 0x28, 0x28, 0x28, 0x28, 0x28,
    0x28, 0x28, 0x28, 0x28, 0x28,
    0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28,
    0x28, 0x28, 0x28, 0x28, 0x28,
    0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28,
    0x28, 0x28, 0x28, 0x28, 0x28,
    0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0xff, 0xc4, 0x01,
    0xa2, 0x00, 0x00, 0x01, 0x05,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x01, 0x02,
    0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x01, 0x00,
    0x03, 0x01, 0x01, 0x01, 0x01,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x01, 0x02, 0x03, 0x04, 0x05,
    0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x10, 0x00, 0x02, 0x01, 0x03,
    0x03, 0x02, 0x04, 0x03, 0x05,
    0x05, 0x04, 0x04, 0x00, 0x00, 0x01, 0x7d, 0x01, 0x02, 0x03, 0x00,
    0x04, 0x11, 0x05, 0x12, 0x21,
    0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07, 0x22, 0x71, 0x14, 0x32,
    0x81, 0x91, 0xa1, 0x08, 0x23,
    0x42, 0xb1, 0xc1, 0x15, 0x52, 0xd1, 0xf0, 0x24, 0x33, 0x62, 0x72,
    0x82, 0x09, 0x0a, 0x16, 0x17,
    0x18, 0x19, 0x1a, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2a, 0x34, 0x35,
    0x36, 0x37, 0x38, 0x39, 0x3a,
    0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4a, 0x53, 0x54, 0x55,
    0x56, 0x57, 0x58, 0x59, 0x5a,
    0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x73, 0x74, 0x75,
    0x76, 0x77, 0x78, 0x79, 0x7a,
    0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 0x92, 0x93, 0x94,
    0x95, 0x96, 0x97, 0x98, 0x99,
    0x9a, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6, 0xa7, 0xa8, 0xa9, 0xaa, 0xb2,
    0xb3, 0xb4, 0xb5, 0xb6, 0xb7,
    0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4, 0xc5, 0xc6, 0xc7, 0xc8, 0xc9,
    0xca, 0xd2, 0xd3, 0xd4, 0xd5,
    0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe1, 0xe2, 0xe3, 0xe4, 0xe5, 0xe6,
    0xe7, 0xe8, 0xe9, 0xea, 0xf1,
    0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa, 0x11, 0x00,
    0x02, 0x01, 0x02, 0x04, 0x04,
    0x03, 0x04, 0x07, 0x05, 0x04, 0x04, 0x00, 0x01, 0x02, 0x77, 0x00,
    0x01, 0x02, 0x03, 0x11, 0x04,
    0x05, 0x21, 0x31, 0x06, 0x12, 0x41, 0x51, 0x07, 0x61, 0x71, 0x13,
    0x22, 0x32, 0x81, 0x08, 0x14,
    0x42, 0x91, 0xa1, 0xb1, 0xc1, 0x09, 0x23, 0x33, 0x52, 0xf0, 0x15,
    0x62, 0x72, 0xd1, 0x0a, 0x16,
    0x24, 0x34, 0xe1, 0x25, 0xf1, 0x17, 0x18, 0x19, 0x1a, 0x26, 0x27,
    0x28, 0x29, 0x2a, 0x35, 0x36,
    0x37, 0x38, 0x39, 0x3a, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49,
    0x4a, 0x53, 0x54, 0x55, 0x56,
    0x57, 0x58, 0x59, 0x5a, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69,
    0x6a, 0x73, 0x74, 0x75, 0x76,
    0x77, 0x78, 0x79, 0x7a, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88,
    0x89, 0x8a, 0x92, 0x93, 0x94,
    0x95, 0x96, 0x97, 0x98, 0x99, 0x9a, 0xa2, 0xa3, 0xa4, 0xa5, 0xa6,
    0xa7, 0xa8, 0xa9, 0xaa, 0xb2,
    0xb3, 0xb4, 0xb5, 0xb6, 0xb7, 0xb8, 0xb9, 0xba, 0xc2, 0xc3, 0xc4,
    0xc5, 0xc6, 0xc7, 0xc8, 0xc9,
    0xca, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0xd8, 0xd9, 0xda, 0xe2,
    0xe3, 0xe4, 0xe5, 0xe6, 0xe7,
    0xe8, 0xe9, 0xea, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9,
    0xfa, 0xff, 0xc0, 0x00, 0x11,
    0x08, 0x01, 0xe0, 0x02, 0x80, 0x03, 0x01, 0x21, 0x00, 0x02, 0x11,
    0x01, 0x03, 0x11, 0x01, 0xff,
    0xda, 0x00, 0x0c, 0x03, 0x01, 0x00, 0x02, 0x11, 0x03, 0x11, 0x00,
    0x3f, 0x00
};

#define GSMART_JPG_HUFFMAN_TABLE_LENGTH 0x1A0

const unsigned char GsmartJPEGHuffmanTable[GSMART_JPG_HUFFMAN_TABLE_LENGTH]
    = {
    0x00, 0x00, 0x01, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
    0x0A, 0x0B, 0x01, 0x00, 0x03,
    0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x01,
    0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x10,
    0x00, 0x02, 0x01, 0x03, 0x03,
    0x02, 0x04, 0x03, 0x05, 0x05, 0x04, 0x04, 0x00, 0x00, 0x01, 0x7D,
    0x01, 0x02, 0x03, 0x00, 0x04,
    0x11, 0x05, 0x12, 0x21, 0x31, 0x41, 0x06, 0x13, 0x51, 0x61, 0x07,
    0x22, 0x71, 0x14, 0x32, 0x81,
    0x91, 0xA1, 0x08, 0x23, 0x42, 0xB1, 0xC1, 0x15, 0x52, 0xD1, 0xF0,
    0x24, 0x33, 0x62, 0x72, 0x82,
    0x09, 0x0A, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x25, 0x26, 0x27, 0x28,
    0x29, 0x2A, 0x34, 0x35, 0x36,
    0x37, 0x38, 0x39, 0x3A, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48, 0x49,
    0x4A, 0x53, 0x54, 0x55, 0x56,
    0x57, 0x58, 0x59, 0x5A, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69,
    0x6A, 0x73, 0x74, 0x75, 0x76,
    0x77, 0x78, 0x79, 0x7A, 0x83, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89,
    0x8A, 0x92, 0x93, 0x94, 0x95,
    0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7,
    0xA8, 0xA9, 0xAA, 0xB2, 0xB3,
    0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xC2, 0xC3, 0xC4, 0xC5,
    0xC6, 0xC7, 0xC8, 0xC9, 0xCA,
    0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7, 0xD8, 0xD9, 0xDA, 0xE1, 0xE2,
    0xE3, 0xE4, 0xE5, 0xE6, 0xE7,
    0xE8, 0xE9, 0xEA, 0xF1, 0xF2, 0xF3, 0xF4, 0xF5, 0xF6, 0xF7, 0xF8,
    0xF9, 0xFA, 0x11, 0x00, 0x02,
    0x01, 0x02, 0x04, 0x04, 0x03, 0x04, 0x07, 0x05, 0x04, 0x04, 0x00,
    0x01, 0x02, 0x77, 0x00, 0x01,
    0x02, 0x03, 0x11, 0x04, 0x05, 0x21, 0x31, 0x06, 0x12, 0x41, 0x51,
    0x07, 0x61, 0x71, 0x13, 0x22,
    0x32, 0x81, 0x08, 0x14, 0x42, 0x91, 0xA1, 0xB1, 0xC1, 0x09, 0x23,
    0x33, 0x52, 0xF0, 0x15, 0x62,
    0x72, 0xD1, 0x0A, 0x16, 0x24, 0x34, 0xE1, 0x25, 0xF1, 0x17, 0x18,
    0x19, 0x1A, 0x26, 0x27, 0x28,
    0x29, 0x2A, 0x35, 0x36, 0x37, 0x38, 0x39, 0x3A, 0x43, 0x44, 0x45,
    0x46, 0x47, 0x48, 0x49, 0x4A,
    0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A, 0x63, 0x64, 0x65,
    0x66, 0x67, 0x68, 0x69, 0x6A,
    0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x82, 0x83, 0x84,
    0x85, 0x86, 0x87, 0x88, 0x89,
    0x8A, 0x92, 0x93, 0x94, 0x95, 0x96, 0x97, 0x98, 0x99, 0x9A, 0xA2,
    0xA3, 0xA4, 0xA5, 0xA6, 0xA7,
    0xA8, 0xA9, 0xAA, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9,
    0xBA, 0xC2, 0xC3, 0xC4, 0xC5,
    0xC6, 0xC7, 0xC8, 0xC9, 0xCA, 0xD2, 0xD3, 0xD4, 0xD5, 0xD6, 0xD7,
    0xD8, 0xD9, 0xDA, 0xE2, 0xE3,
    0xE4, 0xE5, 0xE6, 0xE7, 0xE8, 0xE9, 0xEA, 0xF2, 0xF3, 0xF4, 0xF5,
    0xF6, 0xF7, 0xF8, 0xF9, 0xFA
};

const unsigned char GsmartJPEGScanTable[6] = {
    0x01, 0x00,
    0x02, 0x11,
    0x03, 0x11
};
const unsigned char GsmartQTable[][64] = {

    //index0,Q40
    {
     20, 14, 15, 18, 15, 13, 20, 18, 16, 18, 23, 21, 20, 24, 30, 50,
     33, 30, 28, 28, 30, 61, 44, 46, 36, 50, 73, 64, 76, 75, 71, 64,
     70, 69, 80, 90, 115, 98, 80, 85, 109, 86, 69, 70, 100, 136, 101,
     109,
     119, 123, 129, 130, 129, 78, 96, 141, 151, 140, 125, 150, 115,
     126, 129, 124},
    {
     21, 23, 23, 30, 26, 30, 59, 33, 33, 59, 124, 83, 70, 83, 124, 124,
     124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124,
     124, 124, 124,
     124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124,
     124, 124, 124,
     124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124,
     124, 124, 124},
    //index1,Q50
    {
     16, 11, 12, 14, 12, 10, 16, 14, 13, 14, 18, 17, 16, 19, 24, 40,
     26, 24, 22, 22, 24, 49, 35, 37, 29, 40, 58, 51, 61, 60, 57, 51,
     56, 55, 64, 72, 92, 78, 64, 68, 87, 69, 55, 56, 80, 109, 81, 87,
     95, 98, 103, 104, 103, 62, 77, 113, 121, 112, 100, 120, 92, 101,
     103, 99},
    {
     17, 18, 18, 24, 21, 24, 47, 26, 26, 47, 99, 66, 56, 66, 99, 99,
     99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
     99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99},
    //index2,Q60
    {
     13, 9, 10, 11, 10, 8, 13, 11, 10, 11, 14, 14, 13, 15, 19, 32,
     21, 19, 18, 18, 19, 39, 28, 30, 23, 32, 46, 41, 49, 48, 46, 41,
     45, 44, 51, 58, 74, 62, 51, 54, 70, 55, 44, 45, 64, 87, 65, 70,
     76, 78, 82, 83, 82, 50, 62, 90, 97, 90, 80, 96, 74, 81, 82, 79},
    {
     14, 14, 14, 19, 17, 19, 38, 21, 21, 38, 79, 53, 45, 53, 79, 79,
     79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,
     79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79,
     79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79},
    //index3,Q70
    {
     10, 7, 7, 8, 7, 6, 10, 8, 8, 8, 11, 10, 10, 11, 14, 24,
     16, 14, 13, 13, 14, 29, 21, 22, 17, 24, 35, 31, 37, 36, 34, 31,
     34, 33, 38, 43, 55, 47, 38, 41, 52, 41, 33, 34, 48, 65, 49, 52,
     57, 59, 62, 62, 62, 37, 46, 68, 73, 67, 60, 72, 55, 61, 62, 59},
    {
     10, 11, 11, 14, 13, 14, 28, 16, 16, 28, 59, 40, 34, 40, 59, 59,
     59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59,
     59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59,
     59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59, 59},
    //index4,Q80
    {
     6, 4, 5, 6, 5, 4, 6, 6, 5, 6, 7, 7, 6, 8, 10, 16,
     10, 10, 9, 9, 10, 20, 14, 15, 12, 16, 23, 20, 24, 24, 23, 20,
     22, 22, 26, 29, 37, 31, 26, 27, 35, 28, 22, 22, 32, 44, 32, 35,
     38, 39, 41, 42, 41, 25, 31, 45, 48, 45, 40, 48, 37, 40, 41, 40},
    {
     7, 7, 7, 10, 8, 10, 19, 10, 10, 19, 40, 26, 22, 26, 40, 40,
     40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
     40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
     40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40},
    //index5Q85
    {
     5, 3, 4, 4, 4, 3, 5, 4, 4, 4, 5, 5, 5, 6, 7, 12,
     8, 7, 7, 7, 7, 15, 11, 11, 9, 12, 17, 15, 18, 18, 17, 15,
     17, 17, 19, 22, 28, 23, 19, 20, 26, 21, 17, 17, 24, 33, 24, 26,
     29, 29, 31, 31, 31, 19, 23, 34, 36, 34, 30, 36, 28, 30, 31, 30},
    {
     5, 5, 5, 7, 6, 7, 14, 8, 8, 14, 30, 20, 17, 20, 30, 30,
     30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
     30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
     30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30},
/* Qindex= 86 */
{ 0x04, 0x03, 0x03, 0x04, 0x03, 0x03, 0x04, 0x04, 0x04, 0x04, 0x05, 0x05, 0x04, 0x05, 0x07, 0x0B, 
0x07, 0x07, 0x06, 0x06, 0x07, 0x0E, 0x0A, 0x0A, 0x08, 0x0B, 0x10, 0x0E, 0x11, 0x11, 0x10, 0x0E, 
0x10, 0x0F, 0x12, 0x14, 0x1A, 0x16, 0x12, 0x13, 0x18, 0x13, 0x0F, 0x10, 0x16, 0x1F, 0x17, 0x18, 
0x1B, 0x1B, 0x1D, 0x1D, 0x1D, 0x11, 0x16, 0x20, 0x22, 0x1F, 0x1C, 0x22, 0x1A, 0x1C, 0x1D, 0x1C, 
},
{0x05, 0x05, 0x05, 0x07, 0x06, 0x07, 0x0D, 0x07, 0x07, 0x0D, 0x1C, 0x12, 0x10, 0x12, 0x1C, 0x1C, 
0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 
0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 
0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 
 },
    /* Qindex= 88 */
{ 0x04, 0x03, 0x03, 0x03, 0x03, 0x02, 0x04, 0x03, 0x03, 0x03, 0x04, 0x04, 0x04, 0x05, 0x06, 0x0A, 
0x06, 0x06, 0x05, 0x05, 0x06, 0x0C, 0x08, 0x09, 0x07, 0x0A, 0x0E, 0x0C, 0x0F, 0x0E, 0x0E, 0x0C, 
0x0D, 0x0D, 0x0F, 0x11, 0x16, 0x13, 0x0F, 0x10, 0x15, 0x11, 0x0D, 0x0D, 0x13, 0x1A, 0x13, 0x15, 
0x17, 0x18, 0x19, 0x19, 0x19, 0x0F, 0x12, 0x1B, 0x1D, 0x1B, 0x18, 0x1D, 0x16, 0x18, 0x19, 0x18, 
},
{0x04, 0x04, 0x04, 0x06, 0x05, 0x06, 0x0B, 0x06, 0x06, 0x0B, 0x18, 0x10, 0x0D, 0x10, 0x18, 0x18, 
0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 
0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 
0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 
 }

};

int spca50x_outpicture(struct spca50x_frame *myframe);

static int jpeg_decode411(struct spca50x_frame *myframe, int force_rgb);
static int jpeg_decode422(struct spca50x_frame *myframe, int force_rgb);
static int yuv_decode(struct spca50x_frame *myframe, int force_rgb);
static int bayer_decode(struct spca50x_frame *myframe, int force_rgb);
static int make_jpeg(struct spca50x_frame *myframe);
static int make_jpeg_conexant(struct spca50x_frame *myframe);
static int yvyu_translate(struct spca50x_frame *myframe, int force_rgb);


#define CLIP(color) (unsigned char)(((color)>0xFF)?0xff:(((color)<0)?0:(color)))
/****************************************************************/
/**************      Sonix  huffman decoder      ****************/
/****************************************************************/
static inline unsigned char getByte(unsigned char *inp,
				    unsigned int bitpos)
{
    unsigned char *addr;
    addr = inp + (bitpos >> 3);
    return (addr[0] << (bitpos & 7)) | (addr[1] >> (8 - (bitpos & 7)));
}
void init_sonix_decoder(struct usb_spca50x *spca50x)
{
    int i;
    int is_abs, val, len;
    struct code_table_t *table = spca50x->maindecode.table;

    for (i = 0; i < 256; i++) {
	is_abs = 0;
	val = 0;
	len = 0;
	if ((i & 0x80) == 0) {
	    /* code 0 */
	    val = 0;
	    len = 1;
	} else if ((i & 0xE0) == 0x80) {
	    /* code 100 */
	    val = +4;
	    len = 3;
	} else if ((i & 0xE0) == 0xA0) {
	    /* code 101 */
	    val = -4;
	    len = 3;
	} else if ((i & 0xF0) == 0xD0) {
	    /* code 1101 */
	    val = +11;
	    len = 4;
	} else if ((i & 0xF0) == 0xF0) {
	    /* code 1111 */
	    val = -11;
	    len = 4;
	} else if ((i & 0xF8) == 0xC8) {
	    /* code 11001 */
	    val = +20;
	    len = 5;
	} else if ((i & 0xFC) == 0xC0) {
	    /* code 110000 */
	    val = -20;
	    len = 6;
	} else if ((i & 0xFC) == 0xC4) {
	    /* code 110001xx: unknown */
	    val = -1;
	    len = 8;
	} else if ((i & 0xF0) == 0xE0) {
	    /* code 1110xxxx */
	    is_abs = 1;
	    val = (i & 0x0F) << 4;
	    len = 8;
	}
	table[i].is_abs = is_abs;
	table[i].val = val;
	table[i].len = len;
    }
}

static void sonix_decompress(struct spca50x_frame *myframe)
{
    int width = myframe->hdrwidth;
    int height = myframe->hdrheight;
    unsigned char *inp = myframe->data;
    unsigned char *outp = myframe->tmpbuffer;
    struct code_table_t *table = myframe->decoder->table;
    int row, col;
    int val;
    int bitpos;
    unsigned char code;
    bitpos = 0;
    for (row = 0; row < height; row++) {
	col = 0;
	/* first two pixels in first two rows are stored as raw 8-bit */
	if (row < 2) {
	    code = getByte(inp, bitpos);
	    bitpos += 8;
	    *outp++ = code;
	    code = getByte(inp, bitpos);
	    bitpos += 8;
	    *outp++ = code;
	    col += 2;
	}

	while (col < width) {
	    /* get bitcode from bitstream */

	    code = getByte(inp, bitpos);
	    /* update bit position */
	    bitpos += table[code].len;

	    /* calculate pixel value */
	    val = table[code].val;
	    /* unknowcode output nothing BS update 23:10:2005 */
	    if (val == -1)
		continue;
	    if (!table[code].is_abs) {
		/* value is relative to top and left pixel */
		if (col < 2) {
		    /* left column: relative to top pixel */
		    val += outp[-2 * width];
		} else if (row < 2) {
		    /* top row: relative to left pixel */
		    val += outp[-2];
		} else {
		    /* main area: average of left pixel and top pixel */
		    val += (outp[-2] + outp[-2 * width]) / 2;
		    //val += (outp[-2] + outp[-2*width] - outp[-2*width -2]);
		}
	    }

	    /* store pixel */
	    *outp++ = CLIP(val);
	    col++;
	}
    }
}

void init_pixart_decoder(struct usb_spca50x *spca50x)
{
    int i;
    int is_abs, val, len;
    struct code_table_t *table = spca50x->maindecode.table;
    for (i = 0; i < 256; i++) {
	is_abs = 0;
	val = 0;
	len = 0;
	if ((i & 0xC0) == 0) {
	    /* code 00 */
	    val = 0;
	    len = 2;
	} else if ((i & 0xC0) == 0x40) {
	    /* code 01 */
	    val = -5;
	    len = 2;
	} else if ((i & 0xC0) == 0x80) {
	    /* code 10 */
	    val = +5;
	    len = 2;
	} else if ((i & 0xF0) == 0xC0) {
	    /* code 1100 */
	    val = -10;
	    len = 4;
	} else if ((i & 0xF0) == 0xD0) {
	    /* code 1101 */
	    val = +10;
	    len = 4;
	} else if ((i & 0xF8) == 0xE0) {
	    /* code 11100 */
	    val = -15;
	    len = 5;
	} else if ((i & 0xF8) == 0xE8) {
	    /* code 11101 */
	    val = +15;
	    len = 5;
	} else if ((i & 0xFC) == 0xF0) {
	    /* code 111100 */
	    val = -20;
	    len = 6;
	} else if ((i & 0xFC) == 0xF4) {
	    /* code 111101 */
	    val = +20;
	    len = 6;
	} else if ((i & 0xF8) == 0xF8) {
	    /* code 11111xxxxxx */
	    is_abs = 1;
	    val = 0;
	    len = 5;
	}
	table[i].is_abs = is_abs;
	table[i].val = val;
	table[i].len = len;
    }
}

static int
pac_decompress_row(struct code_table_t *table, unsigned char *inp,
		   unsigned char *outp, int width)
{
    int col;
    int val;
    int bitpos;
    unsigned char code;


    /* first two pixels are stored as raw 8-bit */
    *outp++ = inp[2];
    *outp++ = inp[3];
    bitpos = 32;

    /* main decoding loop */
    for (col = 2; col < width; col++) {
	/* get bitcode */

	code = getByte(inp, bitpos);
	bitpos += table[code].len;

	/* calculate pixel value */
	if (table[code].is_abs) {
	    /* absolute value: get 6 more bits */
	    code = getByte(inp, bitpos);
	    bitpos += 6;
	    *outp++ = code & 0xFC;
	} else {
	    /* relative to left pixel */
	    val = outp[-2] + table[code].val;
	    *outp++ = CLIP(val);
	}
    }

    /* return line length, rounded up to next 16-bit word */
    return 2 * ((bitpos + 15) / 16);
}

static void tv8532_preprocess(struct spca50x_frame *myframe)
{
/* we should received a whole frame with header and EOL marker
in myframe->data and return a GBRG pattern in frame->tmpbuffer
 sequence 2bytes header the Alternate pixels bayer GB 4 bytes
 Alternate pixels bayer RG 4 bytes EOL */
    int width = myframe->hdrwidth;
    int height = myframe->hdrheight;
    int src = 0;
    unsigned char *dst = myframe->tmpbuffer;
    unsigned char *data = myframe->data;
    int i;
    int seq1, seq2;

    /* precompute where is the good bayer line */
    if ((((data[src + 3] + data[src + width + 7]) >> 1) +
	 (data[src + 4] >> 2) + (data[src + width + 6] >> 1)) >=
	(((data[src + 2] + data[src + width + 6]) >> 1) +
	 (data[src + 3] >> 2) + (data[src + width + 5] >> 1))) {
	seq1 = 3;
	seq2 = 4;
    } else {
	seq1 = 2;
	seq2 = 5;
    }
    for (i = 0; i < height / 2; i++) {
	src += seq1;
	memcpy(dst, &myframe->data[src], width);
	src += (width + 3);
	dst += width;
	memcpy(dst, &myframe->data[src], width);
	src += (width + seq2);
	dst += width;
    }
}

static inline unsigned short getShort(unsigned char *pt)
{
    return ((pt[0] << 8) | pt[1]);
}

static int pixart_decompress(struct spca50x_frame *myframe)
{
/* we should received a whole frame with header and EOL marker
in myframe->data and return a GBRG pattern in frame->tmpbuffer
remove the header then copy line by line EOL is set with 0x0f 0xf0 marker
or 0x1e 0xe1 for compressed line*/
    int width = myframe->hdrwidth;
    int height = myframe->hdrheight;
    unsigned char *outp = myframe->tmpbuffer;
    unsigned char *inp = myframe->data;
    struct code_table_t *table = myframe->decoder->table;
    unsigned short word;
    int row;
    /* skip header */
    inp += 16;
    /* and ask to go at pixel +1 ?? */
    outp++;

    /* iterate over all rows */
    for (row = 0; row < height; row++) {
	word = getShort(inp);
	switch (word) {
	case 0x0FF0:
	    memcpy(outp, inp + 2, width);
	    inp += (2 + width);
	    break;
	case 0x1EE1:
	    inp += pac_decompress_row(table, inp, outp, width);
	    break;

	default:

	    return -1;
	}
	outp += width;
    }

    return 0;
}

/*
#	Decoder for compressed spca561 images			    		#
#	It was developed for "Labtec WebCam Elch 2(SPCA561A)" (046d:0929)	#
#	but it might work with other spca561 cameras				#
*/

static unsigned int bit_bucket;
static unsigned char *input_ptr;

static inline void refill(int *bitfill)
{
    if (*bitfill < 8) {
	bit_bucket = (bit_bucket << 8) | *(input_ptr++);
	*bitfill += 8;
    }
}

static inline int nbits(int *bitfill, int n)
{
    bit_bucket = (bit_bucket << 8) | *(input_ptr++);
    *bitfill -= n;
    return (bit_bucket >> (*bitfill & 0xff)) & ((1 << n) - 1);
}

static inline int _nbits(int *bitfill, int n)
{
    *bitfill -= n;
    return (bit_bucket >> (*bitfill & 0xff)) & ((1 << n) - 1);
}

static int fun_A(int *bitfill)
{
    int ret;
    static int tab[] =
	{ 12, 13, 14, 15, 16, 17, 18, 19, -12, -13, -14, -15, -16, -17,
	-18, -19, -19
    };

    ret = tab[nbits(bitfill, 4)];

    refill(bitfill);
    return ret;
}
static int fun_B(int *bitfill)
{
    static int tab1[] =
	{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 31, 31,
	31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 16, 17,
	18,
	19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30
    };
    static int tab[] =
	{ 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, -5,
	-6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19
    };
    unsigned int tmp;

    tmp = nbits(bitfill, 7) - 68;
    refill(bitfill);
    if (tmp > 47)
	return 0xff;
    return tab[tab1[tmp]];
}
static int fun_C(int *bitfill, int gkw)
{
    static int tab1[] =
	{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 23, 23, 23, 23, 23, 23,
	23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 12, 13,
	14,
	15, 16, 17, 18, 19, 20, 21, 22
    };
    static int tab[] =
	{ 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, -9, -10, -11,
	-12, -13, -14, -15, -16, -17, -18, -19
    };
    unsigned int tmp;

    if (gkw == 0xfe) {

	if (nbits(bitfill, 1) == 0)
	    return 7;
	else
	    return -8;
    }

    if (gkw != 0xff)
	return 0xff;

    tmp = nbits(bitfill, 7) - 72;
    if (tmp > 43)
	return 0xff;

    refill(bitfill);
    return tab[tab1[tmp]];
}
static int fun_D(int *bitfill, int gkw)
{
    if (gkw == 0xfd) {
	if (nbits(bitfill, 1) == 0)
	    return 12;
	else
	    return -13;
    }

    if (gkw == 0xfc) {
	if (nbits(bitfill, 1) == 0)
	    return 13;
	else
	    return -14;
    }

    if (gkw == 0xfe) {
	switch (nbits(bitfill, 2)) {
	case 0:
	    return 14;
	case 1:
	    return -15;
	case 2:
	    return 15;
	case 3:
	    return -16;
	}

    }

    if (gkw == 0xff) {
	switch (nbits(bitfill, 3)) {
	case 4:
	    return 16;
	case 5:
	    return -17;
	case 6:
	    return 17;
	case 7:
	    return -18;
	case 2:
	    return _nbits(bitfill, 1) ? 0xed : 0x12;
	case 3:
	    (*bitfill)--;
	    return 18;
	}

	return 0xff;
    }
    return gkw;
}

static int fun_E(int cur_byte, int *bitfill)
{
    static int tab0[] = { 0, -1, 1, -2, 2, -3, 3, -4 };
    static int tab1[] = { 4, -5, 5, -6, 6, -7, 7, -8 };
    static int tab2[] = { 8, -9, 9, -10, 10, -11, 11, -12 };
    static int tab3[] = { 12, -13, 13, -14, 14, -15, 15, -16 };
    static int tab4[] = { 16, -17, 17, -18, 18, -19, 19, -19 };

    if ((cur_byte & 0xf0) >= 0x80) {
	*bitfill -= 4;
	return tab0[(cur_byte >> 4) & 7];
    } else if ((cur_byte & 0xc0) == 0x40) {
	*bitfill -= 5;
	return tab1[(cur_byte >> 3) & 7];

    } else if ((cur_byte & 0xe0) == 0x20) {
	*bitfill -= 6;
	return tab2[(cur_byte >> 2) & 7];

    } else if ((cur_byte & 0xf0) == 0x10) {
	*bitfill -= 7;
	return tab3[(cur_byte >> 1) & 7];

    } else if ((cur_byte & 0xf8) == 8) {
	*bitfill -= 8;
	return tab4[cur_byte & 7];
    }

    return 0xff;
}

static int fun_F(int cur_byte, int *bitfill)
{
    *bitfill -= 5;
    switch (cur_byte & 0xf8) {
    case 0x80:
	return 0;
    case 0x88:
	return -1;
    case 0x90:
	return 1;
    case 0x98:
	return -2;
    case 0xa0:
	return 2;
    case 0xa8:
	return -3;
    case 0xb0:
	return 3;
    case 0xb8:
	return -4;
    case 0xc0:
	return 4;
    case 0xc8:
	return -5;
    case 0xd0:
	return 5;
    case 0xd8:
	return -6;
    case 0xe0:
	return 6;
    case 0xe8:
	return -7;
    case 0xf0:
	return 7;
    case 0xf8:
	return -8;
    }

    *bitfill -= 1;

    switch (cur_byte & 0xfc) {
    case 0x40:
	return 8;
    case 0x44:
	return -9;
    case 0x48:
	return 9;
    case 0x4c:
	return -10;
    case 0x50:
	return 10;
    case 0x54:
	return -11;
    case 0x58:
	return 11;
    case 0x5c:
	return -12;
    case 0x60:
	return 12;
    case 0x64:
	return -13;
    case 0x68:
	return 13;
    case 0x6c:
	return -14;
    case 0x70:
	return 14;
    case 0x74:
	return -15;
    case 0x78:
	return 15;
    case 0x7c:
	return -16;
    }

    *bitfill -= 1;

    switch (cur_byte & 0xfe) {
    case 0x20:
	return 16;
    case 0x22:
	return -17;
    case 0x24:
	return 17;
    case 0x26:
	return -18;
    case 0x28:
	return 18;
    case 0x2a:
	return -19;
    case 0x2c:
	return 19;
    }

    *bitfill += 7;
    return 0xff;
}
int internal_spca561_decode(int width, int height, unsigned char *inbuf, unsigned char *outbuf)	// {{{
{
    // buffers
    static int accum[8 * 8 * 8];
    static int i_hits[8 * 8 * 8];

    const static int nbits_A[] =
	{ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1,
	8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 7, 7, 7, 7,
	7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
	5, 5, 5, 5, 5,
	5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    };
    const static int tab_A[] =
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 11, -11, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10,
	255, 254, -4,
	-4, -5, -5, -6, -6, -7, -7, -8, -8, -9, -9, -10, -10, -1, -1, -1,
	-1, -1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1,
	-1, -1, -1, -1, -1, -1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3,
	3, 3, 3,
	-2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, 1,
	1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1,
	1
    };

    const static int nbits_B[] =
	{ 0, 8, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4,
	4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    };
    const static int tab_B[] =
	{ 0xff, -4, 3, 3, -3, -3, -3, -3, 2, 2, 2, 2, 2, 2, 2, 2, -2,
	-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, 1, 1,
	1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1,
	-1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0,
    };

    const static int nbits_C[] =
	{ 0, 0, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5,
	5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
	4, 4, 4, 4, 4,
	4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    };
    const static int tab_C[] =
	{ 0xff, 0xfe, 6, -7, 5, 5, -6, -6, 4, 4, 4, 4, -5, -5, -5, -5,
	3, 3, 3, 3, 3, 3, 3, 3, -4, -4, -4, -4, -4, -4, -4, -4, 2, 2, 2, 2,
	2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
	-3, -3, -3,
	-3, -3, -3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2, -2, -2, -2, -2, -2, -2,
	-2, -2, -2,
	-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2,
	-2, -2,
	-2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1,
	-1, -1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    };

    const static int nbits_D[] =
	{ 0, 0, 0, 0, 8, 8, 8, 8, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
	5, 5, 5, 5, 5,
	5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4,
	4, 4, 4, 4, 4,
	4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
	4, 4, 4, 4, 4,
	4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
	4, 4, 4, 4, 4,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
	3, 3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
    };
    const static int tab_D[] =
	{ 0xff, 0xfe, 0xfd, 0xfc, 10, -11, 11, -12, 8, 8, -9, -9, 9, 9,
	-10, -10, 6, 6, 6, 6, -7, -7, -7, -7, 7, 7, 7, 7, -8, -8, -8, -8,
	4, 4, 4, 4,
	4, 4, 4, 4, -5, -5, -5, -5, -5, -5, -5, -5, 5, 5, 5, 5, 5, 5, 5, 5,
	-6, -6,
	-6, -6, -6, -6, -6, -6, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, -3,
	-3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, 3, 3,
	3, 3, 3, 3,
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -4, -4, -4, -4, -4, -4, -4, -4, -4,
	-4, -4, -4,
	-4, -4, -4, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1, -1,
	-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
	-1, -1,
	-1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2,
	-2, -2, -2,
	-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2,
	-2, -2
    };

    // a_curve[19 + i] = ... [-19..19] => [-160..160]
    const static int a_curve[] =
	{ -160, -144, -128, -112, -98, -88, -80, -72, -64, -56, -48,
	-40, -32, -24, -18, -12, -8, -5, -2, 0, 2, 5, 8, 12, 18, 24, 32,
	40, 48, 56, 64,
	72, 80, 88, 98, 112, 128, 144, 160
    };
    // clamp0_255[256 + i] = min(max(i,255),0)
    const static unsigned char clamp0_255[] =
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
	3, 4, 5, 6, 7, 8, 9, 10,
	11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
	28, 29, 30, 31, 32, 33,
	34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
	51, 52, 53, 54, 55, 56,
	57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
	74, 75, 76, 77, 78, 79,
	80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96,
	97, 98, 99, 100, 101,
	102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114,
	115, 116, 117, 118, 119,
	120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132,
	133, 134, 135, 136, 137,
	138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150,
	151, 152, 153, 154, 155,
	156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168,
	169, 170, 171, 172, 173,
	174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186,
	187, 188, 189, 190, 191,
	192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204,
	205, 206, 207, 208, 209,
	210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222,
	223, 224, 225, 226, 227,
	228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240,
	241, 242, 243, 244, 245,
	246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255, 255, 255, 255, 255,
	255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
	255
    };
    // abs_clamp15[19 + i] = min(abs(i), 15)
    const static int abs_clamp15[] =
	{ 15, 15, 15, 15, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3,
	2, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15, 15,
	15
    };
    // diff_encoding[256 + i] = ...
    const static int diff_encoding[] =
	{ 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7,
	7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5,
	5, 5, 5, 5, 5, 3, 3,
	3, 3, 1, 1, 0, 2, 2, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
	6, 6, 6, 6, 6, 6
    };


    int block;

    int bitfill = 0;
    int xwidth = width + 6;
    int off_up_right = 2 - 2 * xwidth;
    int off_up_left = -2 - 2 * xwidth;

    int pixel_U = 0, saved_pixel_UR = 0;
    int pixel_x = 0, pixel_y = 2;

    unsigned char *output_ptr = outbuf;

    memset(i_hits, 0, sizeof(i_hits));
    memset(accum, 0, sizeof(accum));

    memcpy(outbuf + xwidth * 2 + 3, inbuf + 0x14, width);
    memcpy(outbuf + xwidth * 3 + 3, inbuf + 0x14 + width, width);

    input_ptr = inbuf + 0x14 + width * 2;
    output_ptr = outbuf + (xwidth) * 4 + 3;

    bit_bucket = 0;

    for (block = 0; block < ((height - 2) * width) / 32; ++block) {
	int b_it, var_7 = 0;
	int cur_byte;

	refill(&bitfill);

	cur_byte = (bit_bucket >> (bitfill & 7)) & 0xff;

	if ((cur_byte & 0x80) == 0) {
	    var_7 = 0;
	    bitfill--;
	} else if ((cur_byte & 0xC0) == 0x80) {
	    var_7 = 1;
	    bitfill -= 2;
	} else if ((cur_byte & 0xc0) == 0xc0) {
	    var_7 = 2;
	    bitfill -= 2;
	}

	for (b_it = 0; b_it < 32; b_it++) {
	    int index;
	    int pixel_L, pixel_UR, pixel_UL;
	    int multiplier;
	    int dL, dC, dR;

	    int gkw;		// God knows what

	    refill(&bitfill);
	    cur_byte = bit_bucket >> (bitfill & 7) & 0xff;

	    pixel_L = output_ptr[-2];
	    pixel_UR = output_ptr[off_up_right];
	    pixel_UL = output_ptr[off_up_left];

	    dL = diff_encoding[0x100 + pixel_UL - pixel_L];
	    dC = diff_encoding[0x100 + pixel_U - pixel_UL];
	    dR = diff_encoding[0x100 + pixel_UR - pixel_U];

	    if (pixel_x < 2) {
		pixel_L = pixel_UL = pixel_U = output_ptr[-xwidth * 2];
		pixel_UR = output_ptr[off_up_right];
		dL = dC = 0;
		dR = diff_encoding[0x100 + pixel_UR - pixel_U];
	    } else if (pixel_x > width - 3)
		dR = 0;

	    multiplier = 4;
	    index = dR + dC * 8 + dL * 64;

	    if (pixel_L + pixel_U * 2 <= 144
		&& (pixel_y & 1) == 0
		&& (b_it & 3) == 0 && (dR < 5) && (dC < 5) && (dL < 5)) {

		multiplier = 1;

	    } else if (pixel_L <= 48
		       && dL <= 4 && dC <= 4 && dL >= 1 && dC >= 1) {
		multiplier = 2;

	    } else if (var_7 == 1) {
		multiplier = 2;

	    } else if (dC + dL >= 11 || var_7 == 2) {
		multiplier = 8;
	    }

	    if (i_hits[index] < 7) {
		bitfill -= nbits_A[cur_byte];
		gkw = tab_A[cur_byte];
		if (gkw == 0xfe)
		    gkw = fun_A(&bitfill);

	    } else if (i_hits[index] >= accum[index]) {
		bitfill -= nbits_B[cur_byte];
		gkw = tab_B[cur_byte];
		if (cur_byte == 0)
		    gkw = fun_B(&bitfill);

	    } else if (i_hits[index] * 2 >= accum[index]) {
		bitfill -= nbits_C[cur_byte];
		gkw = tab_C[cur_byte];
		if (cur_byte < 2)
		    gkw = fun_C(&bitfill, gkw);

	    } else if (i_hits[index] * 4 >= accum[index]) {
		bitfill -= nbits_D[cur_byte];
		gkw = tab_D[cur_byte];
		if (cur_byte < 4)
		    gkw = fun_D(&bitfill, gkw);

	    } else if (i_hits[index] * 8 >= accum[index]) {
		gkw = fun_E(cur_byte, &bitfill);

	    } else {
		gkw = fun_F(cur_byte, &bitfill);
	    }

	    if (gkw == 0xff)
		return -3;

	    {
		int tmp1, tmp2;
		tmp1 = (pixel_U + pixel_L) * 3 - pixel_UL * 2;
		tmp1 += (tmp1 < 0) ? 3 : 0;
		tmp2 = a_curve[19 + gkw] * multiplier;
		tmp2 += (tmp2 < 0) ? 1 : 0;

		*(output_ptr++) =
		    clamp0_255[0x100 + (tmp1 >> 2) - (tmp2 >> 1)];
	    }

	    pixel_U = saved_pixel_UR;
	    saved_pixel_UR = pixel_UR;

	    if (++pixel_x == width) {
		output_ptr += 6;
		pixel_x = 0;
		pixel_y++;
	    }

	    accum[index] += abs_clamp15[19 + gkw];

	    if (i_hits[index]++ == 15) {
		i_hits[index] = 8;
		accum[index] /= 2;
	    }

	}

    }

    return 0;
}
void decode_spca561(unsigned char *inbuf, char *outbuf, int width,
		    int height)
{
    int i;
    static char tmpbuf[650 * 490];

    if (internal_spca561_decode(width, height, inbuf, tmpbuf) == 0) {
	for (i = 0; i < height; i++)
	    memcpy(outbuf + i * width,
		   tmpbuf + (i + 2) * (width + 6) + 3, width);
    }

}

/****************************************************************/
/**************       huffman decoder             ***************/
/****************************************************************/

/*need to be on init jpeg */
static struct comp comp_template[MAXCOMP] = {
    {0x01, 0x22, 0x00},
    {0x02, 0x11, 0x01},
    {0x03, 0x11, 0x01},
    {0x00, 0x00, 0x00}
};

/* deprecated set by webcam now in spca50x */
//static struct scan dscans[MAXCOMP];
//static unsigned char quant[3][64];
//static struct in in;
//int dquant[3][64];
//static struct jpginfo info;
/* table de Huffman global for all */
static struct dec_hufftbl dhuff[4];
#define dec_huffdc (dhuff + 0)
#define dec_huffac (dhuff + 2)
#define M_RST0	0xd0


static int fillbits(struct in *, int, unsigned int);
static int dec_rec2(struct in *, struct dec_hufftbl *, int *, int, int);

static int fillbits(struct in *in, int le, unsigned int bi)
{
    int b;
    int m;
    if (in->marker) {
	if (le <= 16)
	    in->bits = bi << 16, le += 16;
	return le;
    }
    while (le <= 24) {
	b = *in->p++;
	if (in->omitescape) {
	    if (b == 0xff && (m = *in->p++) != 0) {
		in->marker = m;
		if (le <= 16)
		    bi = bi << 16, le += 16;
		break;
	    }
	}
	bi = bi << 8 | b;
	le += 8;
    }
    in->bits = bi;		/* tmp... 2 return values needed */
    return le;
}

#define LEBI_GET(in)	(le = in->left, bi = in->bits)
#define LEBI_PUT(in)	(in->left = le, in->bits = bi)

#define GETBITS(in, n) (					\
  (le < (n) ? le = fillbits(in, le, bi), bi = in->bits : 0),	\
  (le -= (n)),							\
  bi >> le & ((1 << (n)) - 1)					\
)

#define UNGETBITS(in, n) (	\
  le += (n)			\
)

static void dec_initscans(struct dec_data *decode)
{
    struct jpginfo *info = &decode->info;
    struct scan *dscans = decode->dscans;
    int i;
    info->ns = 3;		// HARDCODED  here
    info->nm = info->dri + 1;	// macroblock count
    info->rm = M_RST0;
    for (i = 0; i < info->ns; i++)
	dscans[i].dc = 0;
}
static int dec_readmarker(struct in *in)
{
    int m;

    in->left = fillbits(in, in->left, in->bits);
    if ((m = in->marker) == 0)
	return 0;
    in->left = 0;
    in->marker = 0;
    return m;
}

static int dec_checkmarker(struct dec_data *decode)
{
    struct jpginfo *info = &decode->info;
    struct scan *dscans = decode->dscans;
    struct in *in = &decode->in;
    int i;

    if (dec_readmarker(in) != info->rm)
	return -1;
    info->nm = info->dri;
    info->rm = (info->rm + 1) & ~0x08;
    for (i = 0; i < info->ns; i++)
	dscans[i].dc = 0;
    return 0;
}
void
jpeg_reset_input_context(struct dec_data *decode, unsigned char *buf,
			 int oescap)
{
    /* set input context */
    struct in *in = &decode->in;
    in->p = buf;
    in->omitescape = oescap;
    in->left = 0;
    in->bits = 0;
    in->marker = 0;
}
static int
dec_rec2(struct in *in, struct dec_hufftbl *hu, int *runp, int c, int i)
{
    int le, bi;

    le = in->left;
    bi = in->bits;
    if (i) {
	UNGETBITS(in, i & 127);
	*runp = i >> 8 & 15;
	i >>= 16;
    } else {
	for (i = DECBITS;
	     (c = ((c << 1) | GETBITS(in, 1))) >= (hu->maxcode[i]); i++);
	if (i >= 16) {
	    in->marker = M_BADHUFF;
	    return 0;
	}
	i = hu->vals[hu->valptr[i] + c - hu->maxcode[i - 1] * 2];
	*runp = i >> 4;
	i &= 15;
    }
    if (i == 0) {		/* sigh, 0xf0 is 11 bit */
	LEBI_PUT(in);
	return 0;
    }
    /* receive part */
    c = GETBITS(in, i);
    if (c < (1 << (i - 1)))
	c += (-1 << i) + 1;
    LEBI_PUT(in);
    return c;
}

#define DEC_REC(in, hu, r, i)	 (	\
  r = GETBITS(in, DECBITS),		\
  i = hu->llvals[r],			\
  i & 128 ?				\
    (					\
      UNGETBITS(in, i & 127),		\
      r = i >> 8 & 15,			\
      i >> 16				\
    )					\
  :					\
    (					\
      LEBI_PUT(in),			\
      i = dec_rec2(in, hu, &r, r, i),	\
      LEBI_GET(in),			\
      i					\
    )					\
)

inline static void
decode_mcus(struct in *in, int *dct, int n, struct scan *sc, int *maxp)
{
    struct dec_hufftbl *hu;
    int i, r, t;
    int le, bi;

    memset(dct, 0, n * 64 * sizeof(*dct));
    le = in->left;
    bi = in->bits;

    while (n-- > 0) {
	hu = sc->hudc.dhuff;
	*dct++ = (sc->dc += DEC_REC(in, hu, r, t));

	hu = sc->huac.dhuff;
	i = 63;
	while (i > 0) {
	    t = DEC_REC(in, hu, r, t);
	    if (t == 0 && r == 0) {
		dct += i;
		break;
	    }
	    dct += r;
	    *dct++ = t;
	    i -= r + 1;
	}
	*maxp++ = 64 - i;
	if (n == sc->next)
	    sc++;
    }
    LEBI_PUT(in);
}

static void
dec_makehuff(struct dec_hufftbl *hu, int *hufflen, unsigned char *huffvals)
{
    int code, k, i, j, d, x, c, v;

    for (i = 0; i < (1 << DECBITS); i++)
	hu->llvals[i] = 0;

/*
 * llvals layout:
 *
 * value v already known, run r, backup u bits:
 *  vvvvvvvvvvvvvvvv 0000 rrrr 1 uuuuuuu
 * value unknown, size b bits, run r, backup u bits:
 *  000000000000bbbb 0000 rrrr 0 uuuuuuu
 * value and size unknown:
 *  0000000000000000 0000 0000 0 0000000
 */
    code = 0;
    k = 0;
    for (i = 0; i < 16; i++, code <<= 1) {	/* sizes */
	hu->valptr[i] = k;
	for (j = 0; j < hufflen[i]; j++) {
	    hu->vals[k] = *huffvals++;
	    if (i < DECBITS) {
		c = code << (DECBITS - 1 - i);
		v = hu->vals[k] & 0x0f;	/* size */
		for (d = 1 << (DECBITS - 1 - i); --d >= 0;) {
		    if (v + i < DECBITS) {	/* both fit in table */
			x = d >> (DECBITS - 1 - v - i);
			if (v && x < (1 << (v - 1)))
			    x += (-1 << v) + 1;
			x = x << 16 | (hu->vals[k] & 0xf0)
			    << 4 | (DECBITS - (i + 1 + v)) | 128;
		    } else
			x = v << 16 | (hu->vals[k] & 0xf0)
			    << 4 | (DECBITS - (i + 1));
		    hu->llvals[c | d] = x;
		}
	    }
	    code++;
	    k++;
	}
	hu->maxcode[i] = code;
    }
    hu->maxcode[16] = 0x20000;	/* always terminate decode */
}

/****************************************************************/
/**************             idct                  ***************/
/****************************************************************/


#define S22 ((long)IFIX(2 * 0.382683432))
#define C22 ((long)IFIX(2 * 0.923879532))
#define IC4 ((long)IFIX(1 / 0.707106781))

static unsigned char zig2[64] = {
    0, 2, 3, 9, 10, 20, 21, 35,
    14, 16, 25, 31, 39, 46, 50, 57,
    5, 7, 12, 18, 23, 33, 37, 48,
    27, 29, 41, 44, 52, 55, 59, 62,
    15, 26, 30, 40, 45, 51, 56, 58,
    1, 4, 8, 11, 19, 22, 34, 36,
    28, 42, 43, 53, 54, 60, 61, 63,
    6, 13, 17, 24, 32, 38, 47, 49
};

static void idct(int *in, int *out, int *quant, long off, int max)
{
    long t0, t1, t2, t3, t4, t5, t6, t7;	// t ;
    long tmp0, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6;
    long tmp[64], *tmpp;
    int i, j, te;
    unsigned char *zig2p;

    t0 = off;
    if (max == 1) {
	t0 += in[0] * quant[0];
	for (i = 0; i < 64; i++)
	    out[i] = ITOINT(t0);
	return;
    }
    zig2p = zig2;
    tmpp = tmp;
    for (i = 0; i < 8; i++) {
	j = *zig2p++;
	t0 += in[j] * (long) quant[j];
	j = *zig2p++;
	t5 = in[j] * (long) quant[j];
	j = *zig2p++;
	t2 = in[j] * (long) quant[j];
	j = *zig2p++;
	t7 = in[j] * (long) quant[j];
	j = *zig2p++;
	t1 = in[j] * (long) quant[j];
	j = *zig2p++;
	t4 = in[j] * (long) quant[j];
	j = *zig2p++;
	t3 = in[j] * (long) quant[j];
	j = *zig2p++;
	t6 = in[j] * (long) quant[j];


	if ((t1 | t2 | t3 | t4 | t5 | t6 | t7) == 0) {

	    tmpp[0 * 8] = t0;
	    tmpp[1 * 8] = t0;
	    tmpp[2 * 8] = t0;
	    tmpp[3 * 8] = t0;
	    tmpp[4 * 8] = t0;
	    tmpp[5 * 8] = t0;
	    tmpp[6 * 8] = t0;
	    tmpp[7 * 8] = t0;

	    tmpp++;
	    t0 = 0;
	    continue;
	}
	//IDCT;
	tmp0 = t0 + t1;
	t1 = t0 - t1;
	tmp2 = t2 - t3;
	t3 = t2 + t3;
	tmp2 = IMULT(tmp2, IC4) - t3;
	tmp3 = tmp0 + t3;
	t3 = tmp0 - t3;
	tmp1 = t1 + tmp2;
	tmp2 = t1 - tmp2;
	tmp4 = t4 - t7;
	t7 = t4 + t7;
	tmp5 = t5 + t6;
	t6 = t5 - t6;
	tmp6 = tmp5 - t7;
	t7 = tmp5 + t7;
	tmp5 = IMULT(tmp6, IC4);
	tmp6 = IMULT((tmp4 + t6), S22);
	tmp4 = IMULT(tmp4, (C22 - S22)) + tmp6;
	t6 = IMULT(t6, (C22 + S22)) - tmp6;
	t6 = t6 - t7;
	t5 = tmp5 - t6;
	t4 = tmp4 - t5;

	tmpp[0 * 8] = tmp3 + t7;	//t0;
	tmpp[1 * 8] = tmp1 + t6;	//t1;
	tmpp[2 * 8] = tmp2 + t5;	//t2;
	tmpp[3 * 8] = t3 + t4;	//t3;
	tmpp[4 * 8] = t3 - t4;	//t4;
	tmpp[5 * 8] = tmp2 - t5;	//t5;
	tmpp[6 * 8] = tmp1 - t6;	//t6;
	tmpp[7 * 8] = tmp3 - t7;	//t7;
	tmpp++;
	t0 = 0;
    }
    for (i = 0, j = 0; i < 8; i++) {
	t0 = tmp[j + 0];
	t1 = tmp[j + 1];
	t2 = tmp[j + 2];
	t3 = tmp[j + 3];
	t4 = tmp[j + 4];
	t5 = tmp[j + 5];
	t6 = tmp[j + 6];
	t7 = tmp[j + 7];
	if ((t1 | t2 | t3 | t4 | t5 | t6 | t7) == 0) {
	    te = ITOINT(t0);
	    out[j + 0] = te;
	    out[j + 1] = te;
	    out[j + 2] = te;
	    out[j + 3] = te;
	    out[j + 4] = te;
	    out[j + 5] = te;
	    out[j + 6] = te;
	    out[j + 7] = te;
	    j += 8;
	    continue;
	}
	//IDCT;
	tmp0 = t0 + t1;
	t1 = t0 - t1;
	tmp2 = t2 - t3;
	t3 = t2 + t3;
	tmp2 = IMULT(tmp2, IC4) - t3;
	tmp3 = tmp0 + t3;
	t3 = tmp0 - t3;
	tmp1 = t1 + tmp2;
	tmp2 = t1 - tmp2;
	tmp4 = t4 - t7;
	t7 = t4 + t7;
	tmp5 = t5 + t6;
	t6 = t5 - t6;
	tmp6 = tmp5 - t7;
	t7 = tmp5 + t7;
	tmp5 = IMULT(tmp6, IC4);
	tmp6 = IMULT((tmp4 + t6), S22);
	tmp4 = IMULT(tmp4, (C22 - S22)) + tmp6;
	t6 = IMULT(t6, (C22 + S22)) - tmp6;
	t6 = t6 - t7;
	t5 = tmp5 - t6;
	t4 = tmp4 - t5;

	out[j + 0] = ITOINT(tmp3 + t7);
	out[j + 1] = ITOINT(tmp1 + t6);
	out[j + 2] = ITOINT(tmp2 + t5);
	out[j + 3] = ITOINT(t3 + t4);
	out[j + 4] = ITOINT(t3 - t4);
	out[j + 5] = ITOINT(tmp2 - t5);
	out[j + 6] = ITOINT(tmp1 - t6);
	out[j + 7] = ITOINT(tmp3 - t7);
	j += 8;
    }

}

static unsigned char zig[64] = {
    0, 1, 5, 6, 14, 15, 27, 28,
    2, 4, 7, 13, 16, 26, 29, 42,
    3, 8, 12, 17, 25, 30, 41, 43,
    9, 11, 18, 24, 31, 40, 44, 53,
    10, 19, 23, 32, 39, 45, 52, 54,
    20, 22, 33, 38, 46, 51, 55, 60,
    21, 34, 37, 47, 50, 56, 59, 61,
    35, 36, 48, 49, 57, 58, 62, 63
};

static int aaidct[8] = {
    IFIX(0.3535533906), IFIX(0.4903926402),
    IFIX(0.4619397663), IFIX(0.4157348062),
    IFIX(0.3535533906), IFIX(0.2777851165),
    IFIX(0.1913417162), IFIX(0.0975451610)
};


inline static void idctqtab(unsigned char *qin, int *qout)
{
    int i, j;

    for (i = 0; i < 8; i++)
	for (j = 0; j < 8; j++)
	    qout[zig[i * 8 + j]] = qin[zig[i * 8 + j]] *
		IMULT(aaidct[i], aaidct[j]);
}

inline static void scaleidctqtab(int *q, int sc)
{
    int i;

    for (i = 0; i < 64; i++)
	q[i] = IMULT(q[i], sc);
}

/* Reduce to the necessary minimum. FIXME */
void init_qTable(struct usb_spca50x *spca50x, unsigned int qIndex)
{
    int i, j;
    /* set up a quantization table */
    for (i = 0; i < 2; i++) {
	for (j = 0; j < 64; j++) {
	    spca50x->maindecode.quant[i][j] =
		GsmartQTable[qIndex * 2 + i][j];
	}
    }
    idctqtab(spca50x->maindecode.
	     quant[spca50x->maindecode.dscans[0].tq],
	     spca50x->maindecode.dquant[0]);
    idctqtab(spca50x->maindecode.
	     quant[spca50x->maindecode.dscans[1].tq],
	     spca50x->maindecode.dquant[1]);
    idctqtab(spca50x->maindecode.
	     quant[spca50x->maindecode.dscans[2].tq],
	     spca50x->maindecode.dquant[2]);
    /* rescale qtab */
    //scaleidctqtab (spca50x->maindecode.dquant[0], IFIX (0.7));
    //scaleidctqtab (spca50x->maindecode.dquant[1], IFIX (0.7));
    //scaleidctqtab (spca50x->maindecode.dquant[2], IFIX (0.7));    
}
void init_jpeg_decoder(struct usb_spca50x *spca50x)
{
    unsigned int i, j, k, l;
    int tc, th, tt, tac, tdc;
    unsigned char *ptr;
    unsigned int qIndex = spca50x->qindex;
    memcpy(spca50x->maindecode.comps, comp_template,
	   MAXCOMP * sizeof(struct comp));
    /* set up the huffman table */
    ptr = (unsigned char *) GsmartJPEGHuffmanTable;
    l = GSMART_JPG_HUFFMAN_TABLE_LENGTH;
    while (l > 0) {
	int hufflen[16];
	unsigned char huffvals[256];

	tc = *ptr++;
	th = tc & 15;
	tc >>= 4;
	tt = tc * 2 + th;
	if (tc > 1 || th > 1) {
	    //printf("died whilst setting up huffman table.\n");
	    //abort();
	}
	for (i = 0; i < 16; i++)
	    hufflen[i] = *ptr++;
	l -= 1 + 16;
	k = 0;
	for (i = 0; i < 16; i++) {
	    for (j = 0; j < (unsigned int) hufflen[i]; j++)
		huffvals[k++] = *ptr++;
	    l -= hufflen[i];
	}
	dec_makehuff(dhuff + tt, hufflen, huffvals);
    }

    /* set up the scan table */
    ptr = (unsigned char *) GsmartJPEGScanTable;
    for (i = 0; i < 3; i++) {
	spca50x->maindecode.dscans[i].cid = *ptr++;
	tdc = *ptr++;
	tac = tdc & 15;
	tdc >>= 4;
	if (tdc > 1 || tac > 1) {
	    //printf("died whilst setting up scan table.\n");
	    //abort();
	}
	/* for each component */
	for (j = 0; j < 3; j++)
	    if (spca50x->maindecode.comps[j].cid ==
		spca50x->maindecode.dscans[i].cid)
		break;

	spca50x->maindecode.dscans[i].hv = spca50x->maindecode.comps[j].hv;
	spca50x->maindecode.dscans[i].tq = spca50x->maindecode.comps[j].tq;
	spca50x->maindecode.dscans[i].hudc.dhuff = dec_huffdc + tdc;
	spca50x->maindecode.dscans[i].huac.dhuff = dec_huffac + tac;
    }

    if (spca50x->maindecode.dscans[0].cid != 1 ||
	spca50x->maindecode.dscans[1].cid != 2 ||
	spca50x->maindecode.dscans[2].cid != 3) {
	//printf("invalid cid found.\n");
	//abort();
    }

    if (spca50x->maindecode.dscans[0].hv != 0x22 ||
	spca50x->maindecode.dscans[1].hv != 0x11 ||
	spca50x->maindecode.dscans[2].hv != 0x11) {
	//printf("invalid hv found.\n");
	//abort();
    }
    spca50x->maindecode.dscans[0].next = 6 - 4;
    spca50x->maindecode.dscans[1].next = 6 - 4 - 1;
    spca50x->maindecode.dscans[2].next = 6 - 4 - 1 - 1;	/* 411 encoding */

    /* set up a quantization table */
    init_qTable(spca50x, qIndex);

}



static int bgr = 0;





/* Gamma correction setting */
/*	Gtable[0][n] -> 2.2
*	Gtable[1][n] -> 1.7
*	Gtable[2][n] -> 1.45
*	Gtable[3][n] -> 1
*	Gtable[4][n] -> 0.6896
*	Gtable[5][n] -> 0.5882
*	Gtable[6][n] -> 0.4545
*	gCor coeff 0..6
*/

int spca50x_outpicture(struct spca50x_frame *myframe)
{				/* general idea keep a frame in the temporary buffer from the tasklet */
    /* decode with native format at input and asked format at output */
    /* myframe->cameratype is the native input format */
    /* myframe->format is the asked format */

    struct pictparam *gCorrect = &myframe->pictsetting;
    unsigned char *red = myframe->decoder->Red;
    unsigned char *green = myframe->decoder->Green;
    unsigned char *blue = myframe->decoder->Blue;
    int width = 0;
    int height = 0;
    int done = 0;
    int i;
    if (gCorrect->change) {
	if (gCorrect->change == 0x01) {
	    /* Gamma setting change compute all case */
	    memcpy(red, &GTable[gCorrect->gamma], 256);
	    memcpy(green, &GTable[gCorrect->gamma], 256);
	    memcpy(blue, &GTable[gCorrect->gamma], 256);
	    for (i = 0; i < 256; i++) {
		red[i] =
		    CLIP(((red[i] +
			   gCorrect->OffRed) * gCorrect->GRed) >> 8);
		green[i] =
		    CLIP(((green[i] +
			   gCorrect->OffGreen) * gCorrect->GGreen) >> 8);
		blue[i] =
		    CLIP(((blue[i] +
			   gCorrect->OffBlue) * gCorrect->GBlue) >> 8);

	    }
	    bgr = gCorrect->force_rgb;
	    gCorrect->change = 0x00;
	}
	if (gCorrect->change == 0x02) {
	    /* Red setting change compute Red Value */
	    memcpy(red, &GTable[gCorrect->gamma], 256);
	    for (i = 0; i < 256; i++) {
		red[i] =
		    CLIP(((red[i] +
			   gCorrect->OffRed) * gCorrect->GRed) >> 8);
	    }
	    gCorrect->change &= ~0x02;
	}
	if (gCorrect->change == 0x04) {
	    /* Green setting change compute Green Value */
	    memcpy(green, &GTable[gCorrect->gamma], 256);
	    for (i = 0; i < 256; i++) {
		green[i] =
		    CLIP(((green[i] +
			   gCorrect->OffGreen) * gCorrect->GGreen) >> 8);
	    }
	    gCorrect->change &= ~0x04;
	}
	if (gCorrect->change == 0x08) {
	    /* Blue setting change compute Blue Value */
	    memcpy(blue, &GTable[gCorrect->gamma], 256);
	    for (i = 0; i < 256; i++) {
		blue[i] =
		    CLIP(((blue[i] +
			   gCorrect->OffBlue) * gCorrect->GBlue) >> 8);
	    }
	    gCorrect->change &= ~0x08;
	}
	if (gCorrect->change == 0x10) {
	    /* force_rgb setting change   */
	    bgr = gCorrect->force_rgb;
	    gCorrect->change &= ~0x10;
	}
    }

    switch (myframe->cameratype) {
    case JPGC:

	height = (myframe->data[11] << 8) | myframe->data[12];
	width = (myframe->data[13] << 8) | myframe->data[14];
	if (myframe->hdrheight != height || myframe->hdrwidth != width)
	    done = ERR_CORRUPTFRAME;
	else {
	    //set info.dri struct should be kmalloc with the
	    // instance camera
	    myframe->decoder->info.dri = myframe->data[5];
	    if (myframe->format == VIDEO_PALETTE_JPEG) {
		memcpy(myframe->tmpbuffer, myframe->data,
		       myframe->scanlength);
		done = make_jpeg_conexant(myframe);
	    } else {
		memcpy(myframe->tmpbuffer,
		       myframe->data + 39, myframe->scanlength - 39);
		done = jpeg_decode422(myframe, bgr);
	    }
	}
	break;
    case JPGH:
	width = (myframe->data[10] << 8) | myframe->data[11];
	height = (myframe->data[12] << 8) | myframe->data[13];
	/* some camera did not respond with the good height ie:Labtec Pro 240 -> 232 */
	if (myframe->hdrwidth != width)
	    done = ERR_CORRUPTFRAME;
	else {
	    // reset info.dri
	    myframe->decoder->info.dri = 0;
	    memcpy(myframe->tmpbuffer, myframe->data + 16,
		   myframe->scanlength - 16);
	    if (myframe->format == VIDEO_PALETTE_JPEG)
		done = make_jpeg(myframe);
	    else
		done = jpeg_decode422(myframe, bgr);
	}
	break;
    case JPGM:
    case JPGS:
	// reset info.dri
	myframe->decoder->info.dri = 0;
	memcpy(myframe->tmpbuffer, myframe->data, myframe->scanlength);
	if (myframe->format == VIDEO_PALETTE_JPEG)
	    done = make_jpeg(myframe);
	else
	    done = jpeg_decode422(myframe, bgr);

	break;
    case JPEG:
	memcpy(myframe->tmpbuffer, myframe->data, myframe->scanlength);
	if (myframe->format == VIDEO_PALETTE_JPEG)
	    done = make_jpeg(myframe);
	else
	    done = jpeg_decode411(myframe, bgr);

	break;
    case YUVY:
    case YUYV:
    case YYUV:
	memcpy(myframe->tmpbuffer, myframe->data, myframe->scanlength);
	done = yuv_decode(myframe, bgr);
	break;
    case YUY2:
    	memcpy(myframe->tmpbuffer, myframe->data, myframe->scanlength);
    	done= yvyu_translate(myframe,bgr);
    	break;
    case PGBRG:
	done = pixart_decompress(myframe);
	if (done < 0)
	    break;
	done = bayer_decode(myframe, bgr);
	break;
    case GBGR:
	/* translate the tv8532 stream into GBRG stream */
	tv8532_preprocess(myframe);
	done = bayer_decode(myframe, bgr);
	break;
    case GBRG:
	memcpy(myframe->tmpbuffer, myframe->data, myframe->scanlength);
	done = bayer_decode(myframe, bgr);
	break;
    case S561:
	if (myframe->data[1] & 0x10)
	    decode_spca561(myframe->data, myframe->tmpbuffer,
			   myframe->width, myframe->height);
	else
	    memcpy(myframe->tmpbuffer, myframe->data + 20,
		   myframe->scanlength);

	done = bayer_decode(myframe, bgr);
	break;
    case SN9C:
	sonix_decompress(myframe);
	done = bayer_decode(myframe, bgr);
	break;
    default:
	done = -1;
	break;
    }
    return done;
}

static int yuv_decode(struct spca50x_frame *myframe, int force_rgb)
{

    int r_offset, g_offset, b_offset;
    int my, mx;			/* scan input surface */
    unsigned char *pic1;	/* output surface */
    __u16 *pix1, *pix2;		/* same for 16 bits output */

    unsigned char *U, *V;	/* chroma output pointer */
    int inuv, inv, pocx;	/* offset chroma input */
    int iny, iny1;		/* offset luma input */
    int nextinline, nextoutline;
    int u1, v1, rg;
    unsigned char y, y1;
    char u, v;
    unsigned char *pic = myframe->data;	/* output surface */
    unsigned char *buf = myframe->tmpbuffer;	/* input surface */
    int width = myframe->hdrwidth;
    int height = myframe->hdrheight;
    int softwidth = myframe->width;
    int softheight = myframe->height;
    //int method = myframe->method;
    int format = myframe->format;
    int cropx1 = myframe->cropx1;
    int cropx2 = myframe->cropx2;
    int cropy1 = myframe->cropy1;
    int cropy2 = myframe->cropy2;
    unsigned char *red = myframe->decoder->Red;
    unsigned char *green = myframe->decoder->Green;
    unsigned char *blue = myframe->decoder->Blue;
    int bpp;
    int framesize, frameUsize;

    framesize = softwidth * softheight;
    frameUsize = framesize >> 2;
    /* rgb or bgr like U or V that's the question */
    if (force_rgb) {
	U = pic + framesize;
	V = U + frameUsize;
	r_offset = 2;
	g_offset = 1;
	b_offset = 0;
    } else {
	V = pic + framesize;
	U = V + frameUsize;
	r_offset = 0;
	g_offset = 1;
	b_offset = 2;
    }
    switch (myframe->cameratype) {
    case YUVY:{
	    iny = 0;			   /********* iny **********/
	    inuv = width;		   /*** inuv **** inv ******/
	    nextinline = 3 * width;
	    inv = (nextinline >> 1);
	    iny1 = width << 1;		   /********* iny1 *********/
	}
	break;
    case YUYV:{
	    iny = 0;			   /********* iny **********/
	    inuv = width;		   /*** inuv **** iny1 *****/
	    nextinline = 3 * width;
	    iny1 = (nextinline >> 1);
	    inv = iny1 + width;		    /*** iny1 **** inv ******/
	}
	break;
    case YYUV:{
	    iny = 0;			   /********* iny **********/
	    iny1 = width;		   /********* iny1 *********/
	    inuv = width << 1;		   /*** inuv **** inv ******/
	    inv = inuv + (width >> 1);
	    nextinline = 3 * width;
	}
	break;
    default:{
	    iny = 0;		/* make compiler happy */
	    iny1 = 0;
	    inuv = 0;
	    inv = 0;
	    nextinline = 0;
	}
	break;
    }

    /* Decode to the correct format. */
    switch (format) {
    case VIDEO_PALETTE_RGB565:
	{
	    bpp = 2;
	    /* initialize */

	    pix1 = (__u16 *) pic;
	    pix2 = pix1 + softwidth;


	    for (my = 0; my < height; my += 2) {
		for (mx = 0, pocx = 0; mx < width; mx += 2, pocx++) {
		    /* test if we need to decode */
		    if ((my >= cropy1)
			&& (my < height - cropy2)
			&& (mx >= cropx1)
			&& (mx < width - cropx2)) {
			/* yes decode */
			if (force_rgb) {
			    u = buf[inuv + pocx];
			    v = buf[inv + pocx];
			} else {
			    v = buf[inuv + pocx];
			    u = buf[inv + pocx];
			}
			v1 = ((v << 10) + (v << 9)) >> 10;
			rg = ((u << 8) + (u << 7) +
			      (v << 9) + (v << 4)) >> 10;
			u1 = ((u << 11) + (u << 4)) >> 10;


			/* top pixel Right */
			y1 = 128 + buf[iny + mx];
			*pix1++ = ((red[CLIP((y1 + v1))]
				    & 0xF8) >> 3 |
				   ((green
				     [CLIP((y1 - rg))] &
				     0xFC) << 3) |
				   ((blue[CLIP((y1 + u1))] & 0xF8) << 8));
			/* top pixel Left */
			y1 = 128 + buf[iny + mx + 1];
			*pix1++ = ((red[CLIP((y1 + v1))]
				    & 0xF8) >> 3 |
				   ((green
				     [CLIP((y1 - rg))] &
				     0xFC) << 3) |
				   ((blue[CLIP((y1 + u1))] & 0xF8) << 8));
			/* bottom pixel Right */
			y1 = 128 + buf[iny1 + mx];
			*pix2++ = ((red[CLIP((y1 + v1))]
				    & 0xF8) >> 3 |
				   ((green
				     [CLIP((y1 - rg))] &
				     0xFC) << 3) |
				   ((blue[CLIP((y1 + u1))] & 0xF8) << 8));
			/* bottom pixel Left */
			y1 = 128 + buf[iny1 + mx + 1];
			*pix2++ = ((red[CLIP((y1 + v1))]
				    & 0xF8) >> 3 |
				   ((green
				     [CLIP((y1 - rg))] &
				     0xFC) << 3) |
				   ((blue[CLIP((y1 + u1))] & 0xF8) << 8));




		    }		// end test decode
		}		// end mx loop
		iny += nextinline;
		inuv += nextinline;
		inv += nextinline;
		iny1 += nextinline;
		if (my >= cropy1) {
		    /* are we in a decode surface move the output pointer */
		    pix1 += softwidth;
		    pix2 += softwidth;
		}

	    }			// end my loop

	}
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	break;
    case VIDEO_PALETTE_RGB32:
    case VIDEO_PALETTE_RGB24:
	{
	    bpp = (format == VIDEO_PALETTE_RGB32) ? 4 : 3;
	    /* initialize */
	    nextoutline = bpp * softwidth;
	    pic1 = pic + nextoutline;


	    for (my = 0; my < height; my += 2) {
		for (mx = 0, pocx = 0; mx < width; mx += 2, pocx++) {
		    /* test if we need to decode */
		    if ((my >= cropy1)
			&& (my < height - cropy2)
			&& (mx >= cropx1)
			&& (mx < width - cropx2)) {
			/* yes decode */
			v = buf[inuv + pocx];
			u = buf[inv + pocx];

			v1 = ((v << 10) + (v << 9)) >> 10;
			rg = ((u << 8) + (u << 7) +
			      (v << 9) + (v << 4)) >> 10;
			u1 = ((u << 11) + (u << 4)) >> 10;

			y = 128 + buf[iny + mx];
			/* top pixel Right */

			pic[r_offset] = red[CLIP((y + v1))];
			pic[g_offset] = green[CLIP((y - rg))];
			pic[b_offset] = blue[CLIP((y + u1))];
			pic += bpp;
			/* top pixel Left */
			y = 128 + buf[iny + mx + 1];
			pic[r_offset] = red[CLIP((y + v1))];
			pic[g_offset] = green[CLIP((y - rg))];
			pic[b_offset] = blue[CLIP((y + u1))];
			pic += bpp;
			/* bottom pixel Right */
			y1 = 128 + buf[iny1 + mx];
			pic1[r_offset] = red[CLIP((y1 + v1))];
			pic1[g_offset] = green[CLIP((y1 - rg))];
			pic1[b_offset] = blue[CLIP((y1 + u1))];
			pic1 += bpp;
			/* bottom pixel Left */
			y1 = 128 + buf[iny1 + mx + 1];
			pic1[r_offset] = red[CLIP((y1 + v1))];
			pic1[g_offset] = green[CLIP((y1 - rg))];
			pic1[b_offset] = blue[CLIP((y1 + u1))];
			pic1 += bpp;




		    }		// end test decode
		}		// end mx loop
		iny += nextinline;
		inuv += nextinline;
		inv += nextinline;
		iny1 += nextinline;
		if (my >= cropy1) {
		    /* are we in a decode surface move the output pointer */
		    pic += nextoutline;
		    pic1 += nextoutline;
		}

	    }			// end my loop
	}
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	break;
    case VIDEO_PALETTE_YUV420P:
	{
	    /* initialize */
	    pic1 = pic + softwidth;

	    for (my = 0; my < height; my += 2) {
		for (mx = 0, pocx = 0; mx < width; mx += 2, pocx++) {
		    /* test if we need to decode */
		    if ((my >= cropy1)
			&& (my < height - cropy2)
			&& (mx >= cropx1)
			&& (mx < width - cropx2)) {
			/* yes decode */
			*V++ = 128 + buf[inuv + pocx];
			*U++ = 128 + buf[inv + pocx];
			*pic++ = 128 + buf[iny + mx];
			*pic++ = 128 + buf[iny + mx + 1];
			*pic1++ = 128 + buf[iny1 + mx];
			*pic1++ = 128 + buf[iny1 + mx + 1];

		    }		// end test decode
		}		// end mx loop
		iny += nextinline;
		inuv += nextinline;
		inv += nextinline;
		iny1 += nextinline;

		if (my >= cropy1) {
		    /* are we in a decode surface move the output pointer */
		    pic += softwidth;
		    pic1 += softwidth;
		}

	    }			// end my loop


	}
	myframe->scanlength = (long) (softwidth * softheight * 3) >> 1;
	break;
    case VIDEO_PALETTE_YUYV:
	bpp = 2;
	nextoutline = bpp * softwidth;
	pic1 = pic + nextoutline;
	for (my = 0; my < height; my += 2) {
	    for (mx = 0, pocx = 0; mx < width; mx += 2, pocx++) {
		/* test if we need to decode */
		if ((my >= cropy1)
		    && (my < height - cropy2)
		    && (mx >= cropx1)
		    && (mx < width - cropx2)) {
		    /* yes decode */
		    *pic++ = 128 + buf[iny + mx];
		    *pic++ = 128 + buf[inuv + pocx];	//V
		    *pic++ = 128 + buf[iny + mx + 1];
		    *pic++ = 128 + buf[inv + pocx];	//U

		    *pic1++ = 128 + buf[iny1 + mx];
		    *pic1++ = 128 + buf[inuv + pocx];	//V   
		    *pic1++ = 128 + buf[iny1 + mx + 1];
		    *pic++ = 128 + buf[inv + pocx];	//U

		}		// end test decode
	    }			// end mx loop
	    iny += nextinline;
	    inuv += nextinline;
	    inv += nextinline;
	    iny1 += nextinline;

	    if (my >= cropy1) {
		/* are we in a decode surface move the output pointer */
		pic += nextoutline;
		pic1 += nextoutline;
	    }

	}			// end my loop

	myframe->scanlength = (long) (softwidth * softheight * 2);
	break;

    default:
	break;
    }				// end case
    return 0;
}

/*
 *    linux/drivers/video/fbcon-jpegdec.c - a tiny jpeg decoder.
 *      
 *      (w) August 2001 by Michael Schroeder, <mls@suse.de>
 *
 *    I severly gutted this beast and hardcoded it to the palette and subset
 *    of jpeg needed for the spca50x driver. Also converted it from K&R style
 *    C to a more modern form ;). Michael can't be blamed for what is left.
 *    All nice features are his, all bugs are mine. - till
 *
 *    Change color space converter for YUVP and RGB -  
 *    Rework the IDCT implementation for best speed, cut test in the loop but instead
 *	more copy and paste code :)
 *    For more details about idct look at :
 *    http://rnvs.informatik.tu-chemnitz.de/~jan/MPEG/HTML/IDCT.html 
 *    12/12/2003 mxhaard@magic.fr
 *	add make jpeg from header (mxhaard 20/09/2004)
 *	add jpeg_decode for 422 stream (mxhaard 01/10/2004)       
 */
static int jpeg_decode411(struct spca50x_frame *myframe, int force_rgb)
{
    int mcusx, mcusy, mx, my;
    int *dcts = myframe->dcts;
    int *out = myframe->out;
    int *max = myframe->max;
//      int i;
    int bpp;
    int framesize, frameUsize;
    int k, j;
    int nextline, nextuv, nextblk, nextnewline;
    unsigned char *pic0, *pic1, *outv, *outu;
    __u16 *pix1, *pix2;
    int picy, picx, pocx, pocy;
    unsigned char *U, *V;
    int *outy, *inv, *inu;
    int outy1, outy2;
    int v, u, y1, v1, u1, u2;
    int r_offset, g_offset, b_offset;

    unsigned char *pic = myframe->data;	/* output surface */
    unsigned char *buf = myframe->tmpbuffer;	/* input surface */
    int width = myframe->hdrwidth;
    int height = myframe->hdrheight;
    int softwidth = myframe->width;
    int softheight = myframe->height;
    //int method = myframe->method;
    int format = myframe->format;
    int cropx1 = myframe->cropx1;
    int cropx2 = myframe->cropx2;
    int cropy1 = myframe->cropy1;
    int cropy2 = myframe->cropy2;
    unsigned char *red = myframe->decoder->Red;
    unsigned char *green = myframe->decoder->Green;
    unsigned char *blue = myframe->decoder->Blue;
    struct dec_data *decode = myframe->decoder;

    if ((height & 15) || (width & 15))
	return 1;
    if (width < softwidth || height < softheight)
	return 1;

    mcusx = width >> 4;
    mcusy = height >> 4;
    framesize = softwidth * softheight;
    frameUsize = framesize >> 2;
    jpeg_reset_input_context(decode, buf, 0);

    /* for each component. Reset dc values. */
    //for (i = 0; i < 3; i++)
    //dscans[i].dc = 0;
    dec_initscans(decode);
    /* rgb or bgr like U or V that's the question */
    if (force_rgb) {
	U = pic + framesize;
	V = U + frameUsize;
	r_offset = 2;
	g_offset = 1;
	b_offset = 0;
    } else {
	V = pic + framesize;
	U = V + frameUsize;
	r_offset = 0;
	g_offset = 1;
	b_offset = 2;
    }

    /* Decode to the correct format. */
    switch (format) {
    case VIDEO_PALETTE_RGB565:
	{
	    bpp = 2;
	    nextline = ((softwidth << 1) - 16);	// *bpp;
	    nextblk = bpp * (softwidth << 4);
	    nextnewline = softwidth;	// *bpp;
	    for (my = 0, picy = 0; my < mcusy; my++) {
		for (mx = 0, picx = 0; mx < mcusx; mx++) {

		    decode_mcus(&decode->in, dcts, 6, decode->dscans, max);
		    if ((my >= cropy1)
			&& (my < mcusy - cropy2)
			&& (mx >= cropx1)
			&& (mx < mcusx - cropx2)) {
			idct(dcts, out,
			     decode->dquant[0], IFIX(128.5), max[0]);
			idct(dcts + 64,
			     out + 64,
			     decode->dquant[0], IFIX(128.5), max[1]);
			idct(dcts + 128,
			     out + 128,
			     decode->dquant[0], IFIX(128.5), max[2]);
			idct(dcts + 192,
			     out + 192,
			     decode->dquant[0], IFIX(128.5), max[3]);
			idct(dcts + 256,
			     out + 256,
			     decode->dquant[1], IFIX(0.5), max[4]);
			idct(dcts + 320,
			     out + 320,
			     decode->dquant[2], IFIX(0.5), max[5]);
			pix1 = (__u16 *) (pic + picx + picy);
			pix2 = pix1 + nextnewline;
			outy = out;
			outy1 = 0;
			outy2 = 8;
			inv = out + 64 * 4;
			inu = out + 64 * 5;
			for (j = 0; j < 8; j++) {
			    for (k = 0; k < 8; k++) {
				if (k == 4) {
				    outy1 += 56;
				    outy2 += 56;
				}
				/* outup 4 pixels */
				/* get the UV colors need to change UV order for force rgb? */
				if (force_rgb) {
				    u = *inv++;
				    v = *inu++;
				} else {
				    v = *inv++;
				    u = *inu++;
				}
				/* MX color space why not? */
				v1 = ((v << 10)
				      + (v << 9))
				    >> 10;
				u1 = ((u <<
				       8) + (u << 7) + (v << 9) + (v << 4))
				    >> 10;
				u2 = ((u << 11)
				      + (u << 4))
				    >> 10;
				/* top pixel Right */
				y1 = outy[outy1++];
				*pix1++ = ((red[CLIP((y1 + v1))]
					    & 0xF8)
					   >> 3 |
					   ((green[CLIP((y1 - u1))] & 0xFC)
					    << 3) | ((blue[CLIP((y1 + u2))]
						      & 0xF8) << 8));
				/* top pixel Left */
				y1 = outy[outy1++];
				*pix1++ = ((red[CLIP((y1 + v1))]
					    & 0xF8)
					   >> 3 |
					   ((green[CLIP((y1 - u1))] & 0xFC)
					    << 3) | ((blue[CLIP((y1 + u2))]
						      & 0xF8) << 8));

				/* bottom pixel Right */
				y1 = outy[outy2++];
				*pix2++ = ((red[CLIP((y1 + v1))]
					    & 0xF8)
					   >> 3 |
					   ((green[CLIP((y1 - u1))] & 0xFC)
					    << 3) | ((blue[CLIP((y1 + u2))]
						      & 0xF8) << 8));
				/* bottom pixel Left */
				y1 = outy[outy2++];
				*pix2++ = ((red[CLIP((y1 + v1))]
					    & 0xF8)
					   >> 3 |
					   ((green[CLIP((y1 - u1))] & 0xFC)
					    << 3) | ((blue[CLIP((y1 + u2))]
						      & 0xF8) << 8));

			    }
			    if (j == 3) {
				outy = out + 128;
			    } else {
				outy += 16;
			    }
			    outy1 = 0;
			    outy2 = 8;
			    pix1 += nextline;
			    pix2 += nextline;

			}
			picx += 16 * bpp;
		    }
		}
		if (my >= cropy1)
		    picy += nextblk;

	    }

	}
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	break;
    case VIDEO_PALETTE_RGB32:
    case VIDEO_PALETTE_RGB24:
	{
	    bpp = (format == VIDEO_PALETTE_RGB32) ? 4 : 3;
	    nextline = bpp * ((softwidth << 1) - 16);
	    nextblk = bpp * (softwidth << 4);
	    nextnewline = bpp * softwidth;
	    for (my = 0, picy = 0; my < mcusy; my++) {
		for (mx = 0, picx = 0; mx < mcusx; mx++) {

		    decode_mcus(&decode->in, dcts, 6, decode->dscans, max);
		    if ((my >= cropy1)
			&& (my < mcusy - cropy2)
			&& (mx >= cropx1)
			&& (mx < mcusx - cropx2)) {
			idct(dcts, out,
			     decode->dquant[0], IFIX(128.5), max[0]);
			idct(dcts + 64,
			     out + 64,
			     decode->dquant[0], IFIX(128.5), max[1]);
			idct(dcts + 128,
			     out + 128,
			     decode->dquant[0], IFIX(128.5), max[2]);
			idct(dcts + 192,
			     out + 192,
			     decode->dquant[0], IFIX(128.5), max[3]);
			idct(dcts + 256,
			     out + 256,
			     decode->dquant[1], IFIX(0.5), max[4]);
			idct(dcts + 320,
			     out + 320,
			     decode->dquant[2], IFIX(0.5), max[5]);
			pic0 = pic + picx + picy;
			pic1 = pic0 + nextnewline;
			outy = out;
			outy1 = 0;
			outy2 = 8;
			inv = out + 64 * 4;
			inu = out + 64 * 5;
			for (j = 0; j < 8; j++) {
			    for (k = 0; k < 8; k++) {
				if (k == 4) {
				    outy1 += 56;
				    outy2 += 56;
				}
				/* outup 4 pixels */
				/* get the UV colors need to change UV order for force rgb? */
				v = *inv++;
				u = *inu++;
				/* MX color space why not? */
				v1 = ((v << 10)
				      + (v << 9))
				    >> 10;
				u1 = ((u <<
				       8) + (u << 7) + (v << 9) + (v << 4))
				    >> 10;
				u2 = ((u << 11)
				      + (u << 4))
				    >> 10;
				/* top pixel Right */
				y1 = outy[outy1++];
				pic0[r_offset] = red[CLIP((y1 + v1))];
				pic0[g_offset] = green[CLIP((y1 - u1))];
				pic0[b_offset] = blue[CLIP((y1 + u2))];
				pic0 += bpp;
				/* top pixel Left */
				y1 = outy[outy1++];
				pic0[r_offset] = red[CLIP((y1 + v1))];
				pic0[g_offset] = green[CLIP((y1 - u1))];
				pic0[b_offset] = blue[CLIP((y1 + u2))];
				pic0 += bpp;
				/* bottom pixel Right */
				y1 = outy[outy2++];
				pic1[r_offset] = red[CLIP((y1 + v1))];
				pic1[g_offset] = green[CLIP((y1 - u1))];
				pic1[b_offset] = blue[CLIP((y1 + u2))];
				pic1 += bpp;
				/* bottom pixel Left */
				y1 = outy[outy2++];
				pic1[r_offset] = red[CLIP((y1 + v1))];
				pic1[g_offset] = green[CLIP((y1 - u1))];
				pic1[b_offset] = blue[CLIP((y1 + u2))];
				pic1 += bpp;

			    }
			    if (j == 3) {
				outy = out + 128;
			    } else {
				outy += 16;
			    }
			    outy1 = 0;
			    outy2 = 8;
			    pic0 += nextline;
			    pic1 += nextline;

			}
			picx += 16 * bpp;
		    }
		}
		if (my >= cropy1)
		    picy += nextblk;

	    }
	}
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	break;
    case VIDEO_PALETTE_YUV420P:
	{
	    nextline = (softwidth << 1) - 16;
	    nextuv = (softwidth >> 1) - 8;
	    nextblk = softwidth << 4;
	    nextnewline = softwidth << 2;
	    for (my = 0, picy = 0, pocy = 0; my < mcusy; my++) {
		for (mx = 0, picx = 0, pocx = 0; mx < mcusx; mx++) {
		    decode_mcus(&decode->in, dcts, 6, decode->dscans, max);
		    if ((my >= cropy1)
			&& (my < mcusy - cropy2)
			&& (mx >= cropx1)
			&& (mx < mcusx - cropx2)) {
			idct(dcts, out,
			     decode->dquant[0], IFIX(128.5), max[0]);
			idct(dcts + 64,
			     out + 64,
			     decode->dquant[0], IFIX(128.5), max[1]);
			idct(dcts + 128,
			     out + 128,
			     decode->dquant[0], IFIX(128.5), max[2]);
			idct(dcts + 192,
			     out + 192,
			     decode->dquant[0], IFIX(128.5), max[3]);
			idct(dcts + 256,
			     out + 256,
			     decode->dquant[1], IFIX(0.5), max[4]);
			idct(dcts + 320,
			     out + 320,
			     decode->dquant[2], IFIX(0.5), max[5]);

			pic0 = pic + picx + picy;
			pic1 = pic0 + softwidth;
			outv = V + (pocx + pocy);
			outu = U + (pocx + pocy);
			outy = out;
			outy1 = 0;
			outy2 = 8;
			inv = out + 64 * 4;
			inu = out + 64 * 5;
			for (j = 0; j < 8; j++) {
			    for (k = 0; k < 8; k++) {
				if (k == 4) {
				    outy1 += 56;
				    outy2 += 56;
				}
				/* outup 4 pixels */

				*pic0++ = CLIP(outy[outy1]);
				outy1++;
				*pic0++ = CLIP(outy[outy1]);
				outy1++;
				*pic1++ = CLIP(outy[outy2]);
				outy2++;
				*pic1++ = CLIP(outy[outy2]);
				outy2++;
				*outv++ = CLIP(128 + *inv);
				inv++;
				*outu++ = CLIP(128 + *inu);
				inu++;
			    }
			    if (j == 3) {
				outy = out + 128;
			    } else {
				outy += 16;
			    }
			    outy1 = 0;
			    outy2 = 8;
			    pic0 += nextline;
			    pic1 += nextline;
			    outv += nextuv;
			    outu += nextuv;
			}
			picx += 16;
			pocx += 8;
		    }
		}
		if (my >= cropy1) {
		    picy += nextblk;
		    pocy += nextnewline;
		}
	    }
	}
	myframe->scanlength = (long) ((softwidth * softheight * 3) >> 1);
	break;
    default:
	break;
    }				// end case
    return 0;
}

static int jpeg_decode422(struct spca50x_frame *myframe, int force_rgb)
{
    int mcusx, mcusy, mx, my;
    int *dcts = myframe->dcts;
    int *out = myframe->out;
    int *max = myframe->max;
    int bpp;
    int framesize, frameUsize;
    int k, j;
    int nextline, nextuv, nextblk, nextnewline;
    unsigned char *pic0, *pic1, *outv, *outu;
    __u16 *pix1, *pix2;
    int picy, picx, pocx, pocy;
    unsigned char *U, *V;
    int *outy, *inv, *inu;
    int outy1, outy2;
    int v, u, y1, v1, u1, u2;
    int r_offset, g_offset, b_offset;

    unsigned char *pic = myframe->data;	/* output surface */
    unsigned char *buf = myframe->tmpbuffer;	/* input surface */
    int width = myframe->hdrwidth;
    int height = myframe->hdrheight;
    int softwidth = myframe->width;
    int softheight = myframe->height;
    //int method = myframe->method;
    int format = myframe->format;
    int cropx1 = myframe->cropx1;
    int cropx2 = myframe->cropx2;
    int cropy1 = myframe->cropy1;
    int cropy2 = myframe->cropy2;
    unsigned char *red = myframe->decoder->Red;
    unsigned char *green = myframe->decoder->Green;
    unsigned char *blue = myframe->decoder->Blue;
    struct dec_data *decode = myframe->decoder;
    if ((height & 7) || (width & 7))
	return 1;
    if (width < softwidth || height < softheight)
	return 1;

    mcusx = width >> 4;
    mcusy = height >> 3;
    framesize = softwidth * softheight;
    frameUsize = framesize >> 2;
    jpeg_reset_input_context(decode, buf, 1);

    /* for each component. Reset dc values. */
    dec_initscans(decode);
    /* rgb or bgr like U or V that's the question */
    if (force_rgb) {
	U = pic + framesize;
	V = U + frameUsize;
	r_offset = 2;
	g_offset = 1;
	b_offset = 0;
    } else {
	V = pic + framesize;
	U = V + frameUsize;
	r_offset = 0;
	g_offset = 1;
	b_offset = 2;
    }

    /* Decode to the correct format. */
    switch (format) {
    case VIDEO_PALETTE_RGB565:
	{
	    bpp = 2;
	    nextline = ((softwidth << 1) - 16);	// *bpp;
	    nextblk = bpp * (softwidth << 3);
	    nextnewline = softwidth;	// *bpp;
	    for (my = 0, picy = 0; my < mcusy; my++) {
		for (mx = 0, picx = 0; mx < mcusx; mx++) {
		    if (decode->info.dri && !--decode->info.nm)
			if (dec_checkmarker(decode))
			    return ERR_WRONG_MARKER;
		    decode_mcus(&decode->in, dcts, 4, decode->dscans, max);
		    if ((my >= cropy1)
			&& (my < mcusy - cropy2)
			&& (mx >= cropx1)
			&& (mx < mcusx - cropx2)) {
			idct(dcts, out,
			     decode->dquant[0], IFIX(128.5), max[0]);
			idct(dcts + 64,
			     out + 64,
			     decode->dquant[0], IFIX(128.5), max[1]);
			idct(dcts + 128,
			     out + 256,
			     decode->dquant[1], IFIX(0.5), max[2]);
			idct(dcts + 192,
			     out + 320,
			     decode->dquant[2], IFIX(0.5), max[3]);

			pix1 = (__u16 *) (pic + picx + picy);
			pix2 = pix1 + nextnewline;
			outy = out;
			outy1 = 0;
			outy2 = 8;
			inv = out + 64 * 4;
			inu = out + 64 * 5;
			for (j = 0; j < 4; j++) {
			    for (k = 0; k < 8; k++) {
				if (k == 4) {
				    outy1 += 56;
				    outy2 += 56;
				}
				/* outup 4 pixels Colors are treated as 411 */
				/* get the UV colors need to change UV order for force rgb? */
				if (force_rgb) {

				    u = *inv++;
				    v = *inu++;
				} else {

				    v = *inv++;
				    u = *inu++;
				}
				/* MX color space why not? */
				v1 = ((v << 10)
				      + (v << 9))
				    >> 10;
				u1 = ((u <<
				       8) + (u << 7) + (v << 9) + (v << 4))
				    >> 10;
				u2 = ((u << 11)
				      + (u << 4))
				    >> 10;
				/* top pixel Right */
				y1 = outy[outy1++];
				*pix1++ = ((red[CLIP((y1 + v1))]
					    & 0xF8)
					   >> 3 |
					   ((green[CLIP((y1 - u1))] & 0xFC)
					    << 3) | ((blue[CLIP((y1 + u2))]
						      & 0xF8) << 8));
				/* top pixel Left */
				y1 = outy[outy1++];
				*pix1++ = ((red[CLIP((y1 + v1))]
					    & 0xF8)
					   >> 3 |
					   ((green[CLIP((y1 - u1))] & 0xFC)
					    << 3) | ((blue[CLIP((y1 + u2))]
						      & 0xF8) << 8));

				/* bottom pixel Right */
				y1 = outy[outy2++];
				*pix2++ = ((red[CLIP((y1 + v1))]
					    & 0xF8)
					   >> 3 |
					   ((green[CLIP((y1 - u1))] & 0xFC)
					    << 3) | ((blue[CLIP((y1 + u2))]
						      & 0xF8) << 8));
				/* bottom pixel Left */
				y1 = outy[outy2++];
				*pix2++ = ((red[CLIP((y1 + v1))]
					    & 0xF8)
					   >> 3 |
					   ((green[CLIP((y1 - u1))] & 0xFC)
					    << 3) | ((blue[CLIP((y1 + u2))]
						      & 0xF8) << 8));

			    }

			    outy += 16;
			    outy1 = 0;
			    outy2 = 8;
			    pix1 += nextline;
			    pix2 += nextline;

			}
			picx += 16 * bpp;
		    }
		}
		if (my >= cropy1)
		    picy += nextblk;

	    }

	}
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	break;
    case VIDEO_PALETTE_RGB32:
    case VIDEO_PALETTE_RGB24:
	{
	    bpp = (format == VIDEO_PALETTE_RGB32) ? 4 : 3;
	    nextline = bpp * ((softwidth << 1) - 16);
	    nextblk = bpp * (softwidth << 3);
	    nextnewline = bpp * softwidth;

	    for (my = 0, picy = 0; my < mcusy; my++) {
		for (mx = 0, picx = 0; mx < mcusx; mx++) {
		    if (decode->info.dri && !--decode->info.nm)
			if (dec_checkmarker(decode))
			    return ERR_WRONG_MARKER;
		    decode_mcus(&decode->in, dcts, 4, decode->dscans, max);
		    if ((my >= cropy1)
			&& (my < mcusy - cropy2)
			&& (mx >= cropx1)
			&& (mx < mcusx - cropx2)) {
			idct(dcts, out,
			     decode->dquant[0], IFIX(128.5), max[0]);
			idct(dcts + 64,
			     out + 64,
			     decode->dquant[0], IFIX(128.5), max[1]);
			idct(dcts + 128,
			     out + 256,
			     decode->dquant[1], IFIX(0.5), max[2]);
			idct(dcts + 192,
			     out + 320,
			     decode->dquant[2], IFIX(0.5), max[3]);

			pic0 = pic + picx + picy;
			pic1 = pic0 + nextnewline;
			outy = out;
			outy1 = 0;
			outy2 = 8;
			inv = out + 64 * 4;
			inu = out + 64 * 5;

			for (j = 0; j < 4; j++) {
			    for (k = 0; k < 8; k++) {
				if (k == 4) {
				    outy1 += 56;
				    outy2 += 56;
				}
				/* outup 4 pixels Colors are treated as 411 */

				v = *inv++;
				u = *inu++;

				/* MX color space why not? */
				v1 = ((v << 10)
				      + (v << 9))
				    >> 10;
				u1 = ((u <<
				       8) + (u << 7) + (v << 9) + (v << 4))
				    >> 10;
				u2 = ((u << 11)
				      + (u << 4))
				    >> 10;
				/* top pixel Right */
				y1 = outy[outy1++];
				pic0[r_offset] = red[CLIP((y1 + v1))];
				pic0[g_offset] = green[CLIP((y1 - u1))];
				pic0[b_offset] = blue[CLIP((y1 + u2))];
				pic0 += bpp;
				/* top pixel Left */
				y1 = outy[outy1++];
				pic0[r_offset] = red[CLIP((y1 + v1))];
				pic0[g_offset] = green[CLIP((y1 - u1))];
				pic0[b_offset] = blue[CLIP((y1 + u2))];
				pic0 += bpp;
				/* bottom pixel Right */
				y1 = outy[outy2++];
				pic1[r_offset] = red[CLIP((y1 + v1))];
				pic1[g_offset] = green[CLIP((y1 - u1))];
				pic1[b_offset] = blue[CLIP((y1 + u2))];
				pic1 += bpp;
				/* bottom pixel Left */
				y1 = outy[outy2++];
				pic1[r_offset] = red[CLIP((y1 + v1))];
				pic1[g_offset] = green[CLIP((y1 - u1))];
				pic1[b_offset] = blue[CLIP((y1 + u2))];
				pic1 += bpp;

			    }

			    outy += 16;
			    outy1 = 0;
			    outy2 = 8;
			    pic0 += nextline;
			    pic1 += nextline;

			}

			picx += 16 * bpp;
		    }
		}
		if (my >= cropy1)
		    picy += nextblk;

	    }

	}
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	break;
    case VIDEO_PALETTE_YUV420P:
	{
	    nextline = (softwidth << 1) - 16;
	    nextuv = (softwidth >> 1) - 8;
	    nextblk = softwidth << 3;
	    nextnewline = softwidth << 1;	//2
	    for (my = 0, picy = 0, pocy = 0; my < mcusy; my++) {
		for (mx = 0, picx = 0, pocx = 0; mx < mcusx; mx++) {
		    if (decode->info.dri && !--decode->info.nm)
			if (dec_checkmarker(decode))
			    return ERR_WRONG_MARKER;
		    decode_mcus(&decode->in, dcts, 4, decode->dscans, max);
		    if ((my >= cropy1)
			&& (my < mcusy - cropy2)
			&& (mx >= cropx1)
			&& (mx < mcusx - cropx2)) {
			idct(dcts, out,
			     decode->dquant[0], IFIX(128.5), max[0]);
			idct(dcts + 64,
			     out + 64,
			     decode->dquant[0], IFIX(128.5), max[1]);
			idct(dcts + 128,
			     out + 256,
			     decode->dquant[1], IFIX(0.5), max[2]);
			idct(dcts + 192,
			     out + 320,
			     decode->dquant[2], IFIX(0.5), max[3]);

			pic0 = pic + picx + picy;
			pic1 = pic0 + softwidth;
			outv = V + (pocx + pocy);
			outu = U + (pocx + pocy);
			outy = out;
			outy1 = 0;
			outy2 = 8;
			inv = out + 64 * 4;
			inu = out + 64 * 5;
			for (j = 0; j < 4; j++) {
			    for (k = 0; k < 8; k++) {
				if (k == 4) {
				    outy1 += 56;
				    outy2 += 56;
				}
				/* outup 4 pixels */

				*pic0++ = CLIP(outy[outy1]);
				outy1++;
				*pic0++ = CLIP(outy[outy1]);
				outy1++;
				*pic1++ = CLIP(outy[outy2]);
				outy2++;
				*pic1++ = CLIP(outy[outy2]);
				outy2++;
				/* maybe one day yuv422P */
				*outv++ = CLIP(128 + *inv);
				inv++;
				*outu++ = CLIP(128 + *inu);
				inu++;
			    }

			    outy += 16;
			    outy1 = 0;
			    outy2 = 8;
			    pic0 += nextline;
			    pic1 += nextline;
			    outv += nextuv;
			    outu += nextuv;
			}
			picx += 16;
			pocx += 8;
		    }
		}
		if (my >= cropy1) {
		    picy += nextblk;
		    pocy += nextnewline;
		}
	    }
	}
	myframe->scanlength = (long) ((softwidth * softheight * 3) >> 1);
	break;
    default:
	break;
    }				// end case
    return 0;
}

// y=0.656g+0.125b+0.226r

#define RGB24_TO_Y(r,g,b) (CLIP(\
	(((g) <<9)+((g)<<7)+((g)<<5)+((b)<<7)+((r)<<8)-((r)<<4)-((r)<<3))>>10))

// v=(r-y)0.656
#define YR_TO_V(r,y) (128 + \
	(((((r)-(y)) << 9 )+(((r)-(y)) << 7 )+(((r)-(y)) << 5 )) >> 10))

// u=(b-y)0.5   
#define YB_TO_U(b,y) (128 + \
	(((b)-(y)) >> 1))

#define PACKRGB16(r,g,b) (__u16) ((((b) & 0xF8) << 8 ) | (((g) & 0xFC) << 3 ) | (((r) & 0xF8) >> 3 ))


static int bayer_decode(struct spca50x_frame *myframe, int force_rgb)
{

    int r_offset, g_offset, b_offset;
    int my, mx;			/* scan input surface */
    unsigned char *pic1;	/* output surface */
    __u16 *pix1, *pix2;		/* same for 16 bits output */
    unsigned char *U, *V;	/* chroma output pointer */
    unsigned char inr, ing1, ing2, inb, ing;	/* srgb input */
    int inl, inl1;		/* offset line input */
    int nextinline, nextoutline;
    unsigned char r, b, y1, y2, y3, y4;
    /*kernel matrix 4x4 */
    unsigned char G00, R10, G20, R30, B01, G02, B03, G31, R32, G13,
	B23, G33;
    unsigned char r1, g1, b1, r2, g2, b2, r3, g3, b3, r4, g4, b4;
    int bpp;

    unsigned char *pic = myframe->data;	/* output surface */
    unsigned char *buf = myframe->tmpbuffer;	/* input surface */
    int width = myframe->hdrwidth;
    int height = myframe->hdrheight;
    int softwidth = myframe->width;
    int softheight = myframe->height;
    //int method = myframe->method;
    int format = myframe->format;
    int cropx1 = myframe->cropx1;
    int cropx2 = myframe->cropx2;
    int cropy1 = myframe->cropy1;
    int cropy2 = myframe->cropy2;
    unsigned char *red = myframe->decoder->Red;
    unsigned char *green = myframe->decoder->Green;
    unsigned char *blue = myframe->decoder->Blue;
    int framesize, frameUsize;
    inr = ing1 = ing2 = ing = inb = r = b = 0;	//compiler maybe happy !!
    framesize = softwidth * softheight;
    frameUsize = framesize >> 2;
    /* rgb or bgr like U or V that's the question */
    if (force_rgb) {
	V = pic + framesize;
	U = V + frameUsize;
	r_offset = 0;
	g_offset = 1;
	b_offset = 2;
    } else {
	U = pic + framesize;
	V = U + frameUsize;
	r_offset = 2;
	g_offset = 1;
	b_offset = 0;
    }
    /* initialize input pointer */
    inl = 0;
    inl1 = width;
    nextinline = width << 1;
    /* Decode to the correct format. */
    switch (format) {
    case VIDEO_PALETTE_RGB565:
	{
	    bpp = 2;
	    /* initialize */
	    pix1 = (__u16 *) pic;
	    pix2 = pix1 + softwidth;
	    for (my = 0; my < height; my += 2) {
		for (mx = 0; mx < width; mx += 2) {
		    /* test if we need to decode */
		    if ((my >= cropy1)
			&& (my < height - cropy2)
			&& (mx >= cropx1)
			&& (mx < width - cropx2)) {
			/* yes decode GBRG */

			g1 = green[buf[inl + mx]];
			b2 = blue[buf[inl + 1 + mx]];
			r3 = red[buf[inl1 + mx]];
			g4 = green[buf[inl1 + 1 + mx]];

			if ((mx == 0) || (my == 0)
			    || (mx == (width - 2))
			    || (my == (height - 2))) {
			    ing = (g1 + g4) >> 1;
			    if (force_rgb) {
				*pix1++ = PACKRGB16(r3, g1, b2);
				*pix1++ = PACKRGB16(r3, ing, b2);
				*pix2++ = PACKRGB16(r3, ing, b2);
				*pix2++ = PACKRGB16(r3, g4, b2);
			    } else {
				*pix1++ = PACKRGB16(b2, g1, r3);
				*pix1++ = PACKRGB16(b2, ing, r3);
				*pix2++ = PACKRGB16(b2, ing, r3);
				*pix2++ = PACKRGB16(b2, g4, r3);
			    }
			} else {
			    G00 = buf[inl + mx - width - 1];
			    R10 = buf[inl + mx - width];
			    G20 = buf[inl + mx - width + 1];
			    R30 = buf[inl + mx - width + 2];
			    B01 = buf[inl + mx - 1];
			    G31 = buf[inl + mx + 2];
			    G02 = buf[inl1 + mx - 1];
			    R32 = buf[inl1 + mx + 2];
			    B03 = buf[inl1 + mx + width - 1];
			    G13 = buf[inl1 + mx + width];
			    B23 = buf[inl1 + mx + width + 1];
			    G33 = buf[inl1 + mx + width + 2];
			    b1 = blue[((B01 + b2) >> 1)];
			    r1 = red[((R10 + r3) >> 1)];
			    r4 = red[((r3 + R32) >> 1)];
			    b4 = blue[((b2 + B23) >> 1)];
			    g2 = green[((g1 + g4 + G31 + G20)
					>> 2)];
			    r2 = red[((R10 + R30 + r3 + R32) >> 2)];
			    g3 = green[((g1 + g4 + G13 + G02)
					>> 2)];
			    b3 = blue[((B01 + b2 + B23 + B03) >> 2)];
			    if (force_rgb) {
				*pix1++ = PACKRGB16(r1, g1, b1);
				*pix1++ = PACKRGB16(r2, g2, b2);
				*pix2++ = PACKRGB16(r3, g3, b3);
				*pix2++ = PACKRGB16(r4, g4, b4);
			    } else {
				*pix1++ = PACKRGB16(b1, g1, r1);
				*pix1++ = PACKRGB16(b2, g2, r2);
				*pix2++ = PACKRGB16(b3, g3, r3);
				*pix2++ = PACKRGB16(b4, g4, r4);
			    }
			}

		    }		// end test decode
		}		// end mx loop
		inl += nextinline;
		inl1 += nextinline;
		if (my >= cropy1) {
		    /* are we in a decode surface move the output pointer */
		    pix1 += (softwidth);
		    pix2 += (softwidth);
		}

	    }			// end my loop

	}
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	break;
    case VIDEO_PALETTE_RGB32:
    case VIDEO_PALETTE_RGB24:
	{
	    bpp = (format == VIDEO_PALETTE_RGB32) ? 4 : 3;
	    /* initialize */
	    nextoutline = bpp * softwidth;
	    pic1 = pic + nextoutline;
	    for (my = 0; my < height; my += 2) {
		for (mx = 0; mx < width; mx += 2) {
		    /* test if we need to decode */
		    if ((my >= cropy1)
			&& (my < height - cropy2)
			&& (mx >= cropx1)
			&& (mx < width - cropx2)) {
			/* yes decode GBRG */
			g1 = green[buf[inl + mx]];
			b2 = blue[buf[inl + 1 + mx]];
			r3 = red[buf[inl1 + mx]];
			g4 = green[buf[inl1 + 1 + mx]];

			if ((mx == 0) || (my == 0)
			    || (mx == (width - 2))
			    || (my == (height - 2))) {
			    ing = (g1 + g4) >> 1;
			    /* top pixel Right */

			    pic[r_offset] = r3;
			    pic[g_offset] = g1;
			    pic[b_offset] = b2;
			    pic += bpp;
			    /* top pixel Left */

			    pic[r_offset] = r3;
			    pic[g_offset] = ing;
			    pic[b_offset] = b2;
			    pic += bpp;
			    /* bottom pixel Right */

			    pic1[r_offset] = r3;
			    pic1[g_offset] = ing;
			    pic1[b_offset] = b2;
			    pic1 += bpp;
			    /* bottom pixel Left */

			    pic1[r_offset] = r3;
			    pic1[g_offset] = g4;
			    pic1[b_offset] = b2;
			    pic1 += bpp;
			} else {
			    G00 = buf[inl + mx - width - 1];
			    R10 = buf[inl + mx - width];
			    G20 = buf[inl + mx - width + 1];
			    R30 = buf[inl + mx - width + 2];
			    B01 = buf[inl + mx - 1];
			    G31 = buf[inl + mx + 2];
			    G02 = buf[inl1 + mx - 1];
			    R32 = buf[inl1 + mx + 2];
			    B03 = buf[inl1 + mx + width - 1];
			    G13 = buf[inl1 + mx + width];
			    B23 = buf[inl1 + mx + width + 1];
			    G33 = buf[inl1 + mx + width + 2];
			    b1 = blue[((B01 + b2) >> 1)];
			    r1 = red[((R10 + r3) >> 1)];
			    r4 = red[((r3 + R32) >> 1)];
			    b4 = blue[((b2 + B23) >> 1)];
			    g2 = green[((g1 + g4 + G31 + G20)
					>> 2)];
			    r2 = red[((R10 + R30 + r3 + R32) >> 2)];
			    g3 = green[((g1 + g4 + G13 + G02)
					>> 2)];
			    b3 = blue[((B01 + b2 + B23 + B03) >> 2)];
			    /* top pixel Right */

			    pic[r_offset] = r1;
			    pic[g_offset] = g1;
			    pic[b_offset] = b1;
			    pic += bpp;
			    /* top pixel Left */

			    pic[r_offset] = r2;
			    pic[g_offset] = g2;
			    pic[b_offset] = b2;
			    pic += bpp;
			    /* bottom pixel Right */

			    pic1[r_offset] = r3;
			    pic1[g_offset] = g3;
			    pic1[b_offset] = b3;
			    pic1 += bpp;
			    /* bottom pixel Left */

			    pic1[r_offset] = r4;
			    pic1[g_offset] = g4;
			    pic1[b_offset] = b4;
			    pic1 += bpp;
			}

		    }		// end test decode
		}		// end mx loop
		inl += nextinline;
		inl1 += nextinline;

		if (my >= cropy1) {
		    /* are we in a decode surface move the output pointer */
		    pic += (nextoutline);
		    pic1 += (nextoutline);
		}

	    }			// end my loop
	}
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	break;
    case VIDEO_PALETTE_YUV420P:
	{			/* Not yet implemented */
	    nextoutline = softwidth;
	    pic1 = pic + nextoutline;
	    for (my = 0; my < height; my += 2) {
		for (mx = 0; mx < width; mx += 2) {
		    /* test if we need to decode */
		    if ((my >= cropy1)
			&& (my < height - cropy2)
			&& (mx >= cropx1)
			&& (mx < width - cropx2)) {
			g1 = green[buf[inl + mx]];
			b2 = blue[buf[inl + 1 + mx]];
			r3 = red[buf[inl1 + mx]];
			g4 = green[buf[inl1 + 1 + mx]];

			if ((mx == 0) || (my == 0)
			    || (mx == (width - 2))
			    || (my == (height - 2))) {
			    ing = (g1 + g4) >> 1;
			    /* top pixel Right */
			    y1 = RGB24_TO_Y(r3, g1, b2);
			    *pic++ = y1;
			    /* top pixel Left */
			    y2 = RGB24_TO_Y(r3, ing, b2);
			    *pic++ = y2;
			    /* bottom pixel Right */
			    y3 = RGB24_TO_Y(r3, ing, b2);
			    *pic1++ = y3;
			    /* bottom pixel Left */
			    y4 = RGB24_TO_Y(r3, g4, b2);
			    *pic1++ = y4;
			    /* U V plane */
			    *U++ = YB_TO_U(b2, ((y1 + y4)
						>> 1));
			    *V++ = YR_TO_V(r3, ((y1 + y4)
						>> 1));
			} else {
			    G00 = buf[inl + mx - width - 1];
			    R10 = buf[inl + mx - width];
			    G20 = buf[inl + mx - width + 1];
			    R30 = buf[inl + mx - width + 2];
			    B01 = buf[inl + mx - 1];
			    G31 = buf[inl + mx + 2];
			    G02 = buf[inl1 + mx - 1];
			    R32 = buf[inl1 + mx + 2];
			    B03 = buf[inl1 + mx + width - 1];
			    G13 = buf[inl1 + mx + width];
			    B23 = buf[inl1 + mx + width + 1];
			    G33 = buf[inl1 + mx + width + 2];
			    b1 = blue[((B01 + b2) >> 1)];
			    r1 = red[((R10 + r3) >> 1)];
			    r4 = red[((r3 + R32) >> 1)];
			    b4 = blue[((b2 + B23) >> 1)];
			    g2 = green[((g1 + g4 + G31 + G20)
					>> 2)];
			    r2 = red[((R10 + R30 + r3 + R32) >> 2)];
			    g3 = green[((g1 + g4 + G13 + G02)
					>> 2)];
			    b3 = blue[((B01 + b2 + B23 + B03) >> 2)];
			    /* top pixel Right */
			    y1 = RGB24_TO_Y(r1, g1, b1);
			    *pic++ = y1;
			    /* top pixel Left */
			    y2 = RGB24_TO_Y(r2, g2, b2);
			    *pic++ = y2;
			    /* bottom pixel Right */
			    y3 = RGB24_TO_Y(r3, g3, b3);
			    *pic1++ = y3;
			    /* bottom pixel Left */
			    y4 = RGB24_TO_Y(r4, g4, b4);
			    *pic1++ = y4;
			    /* U V plane */
			    *U++ = YB_TO_U(((b1 + b2 + b3 + b4)
					    >> 2), ((y1 + y2 + y3 + y4)
						    >> 2));
			    *V++ = YR_TO_V(((r1 + r2 + r3 + r4)
					    >> 2), ((y1 + y2 + y3 + y4)
						    >> 2));
			}

		    }		// end test decode
		}		// end mx loop
		inl += nextinline;
		inl1 += nextinline;

		if (my >= cropy1) {
		    /* are we in a decode surface move the output pointer */
		    pic += softwidth;
		    pic1 += softwidth;
		}

	    }			// end my loop

	}
	myframe->scanlength = (long) ((softwidth * softheight * 3) >> 1);
	break;
    default:
	break;
    }				// end case
    return 0;
}				// end bayer_decode


static int yvyu_translate(struct spca50x_frame *myframe, int force_rgb)
{

    int r_offset, g_offset, b_offset;
    int my, mx;			/* scan input surface */ 
   __u16 *pix;		/* same for 16 bits output */
    int bpp;
    int inl,inl1;
    unsigned char *pic = myframe->data;	/* output surface */
    unsigned char *pic1;	/* output surface */
    unsigned char *U, *V;	/* chroma output pointer */
    unsigned char *buf = myframe->tmpbuffer;	/* input surface */
    int width = myframe->hdrwidth;
    int height = myframe->hdrheight;
    int softwidth = myframe->width;
    int softheight = myframe->height;
    //int method = myframe->method;
    int nextinline, nextoutline;
    int format = myframe->format;
    int cropx1 = myframe->cropx1;
    int cropx2 = myframe->cropx2;
    int cropy1 = myframe->cropy1;
    int cropy2 = myframe->cropy2;
    unsigned char *red = myframe->decoder->Red;
    unsigned char *green = myframe->decoder->Green;
    unsigned char *blue = myframe->decoder->Blue;
    int u1, v1, rg;
    unsigned char y;
	char u, v;
    char r, g, b;
    int framesize, frameUsize;

    framesize = softwidth * softheight;
    frameUsize = framesize >> 2;
   // int framesize;
    
    //framesize = softwidth * softheight * 2;
    /* rgb or bgr like U or V that's the question */
    if (force_rgb) {
    	U = pic + framesize;
	V = U + frameUsize;
	r_offset = 0;
	g_offset = 1;
	b_offset = 2;
    } else {
    	V = pic + framesize;
	U = V + frameUsize;
	r_offset = 2;
	g_offset = 1;
	b_offset = 0;
    }
    /* initialize input pointer */
    inl = 0;
    inl1= width << 1;
    pic1= pic+softwidth;
    nextinline = width << 1;
    nextoutline = softwidth;
    /* Decode to the correct format. */
    switch (format) {
   case VIDEO_PALETTE_RGB565:
	{
	    bpp = 2;
	    /* initialize */
	    pix = (__u16 *) pic;

	    for (my = 0; my < height; my ++) {
		for (mx = 0; mx < width; mx += 2) {
		    /* test if we need to decode */
		    if ((my >= cropy1)
			&& (my < height - cropy2)
			&& (mx >= cropx1)
			&& (mx < width - cropx2)) {
			/* yes decode yvyu */
			v=buf[inl+mx*2+1]-0x80;
			u=buf[inl+mx*2+3]-0x80;
			v1 = ((v << 10) + (v << 9)) >> 10;
			rg = ((u << 8) + (u << 7) +
			      (v << 9) + (v << 4)) >> 10;
			u1 = ((u << 11) + (u << 4)) >> 10;
			y = buf[inl+mx*2+0];
			r = red[CLIP((y + v1))];
			g = green[CLIP((y - rg))];
			b = blue[CLIP((y + u1))];
			if (force_rgb)
			    *pix++ = PACKRGB16(r, g, b);
			else
			    *pix++ = PACKRGB16(b, g, r);
			y = buf[inl+mx*2+2];
			r = red[CLIP((y + v1))];
		    	g = green[CLIP((y - rg))];
			b = blue[CLIP((y + u1))];
			if (force_rgb)
			    *pix++ = PACKRGB16(r, g, b);
			else
			    *pix++ = PACKRGB16(b, g, r);
			
		    }
		}		// end mx loop
		inl += nextinline;
	    }			// end my loop

	}
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	break;
   case VIDEO_PALETTE_RGB32:
   case VIDEO_PALETTE_RGB24:
	{
	    bpp = (format == VIDEO_PALETTE_RGB32) ? 4 : 3;
	    /* initialize */
	    nextoutline = bpp * softwidth;
	    for (my = 0; my < height; my ++ ) {
		for (mx = 0; mx < width; mx += 2) {
		    /* test if we need to decode */
		    if ((my >= cropy1)
			&& (my < height - cropy2)
			&& (mx >= cropx1)
			&& (mx < width - cropx2)) {
			/* yes decode yvyu */
			v=buf[inl+mx*2+1]-0x80;
			u=buf[inl+mx*2+3]-0x80;
			v1 = ((v << 10) + (v << 9)) >> 10;
			rg = ((u << 8) + (u << 7) +
			      (v << 9) + (v << 4)) >> 10;
			u1 = ((u << 11) + (u << 4)) >> 10;
			y = buf[inl+mx*2+0];
		
			pic[r_offset] = red[CLIP((y + v1))];
			pic[g_offset] = green[CLIP((y - rg))];
			pic[b_offset] = blue[CLIP((y + u1))];
			pic+=bpp;
			y = buf[inl+mx*2+2];
			pic[r_offset] = red[CLIP((y + v1))];
		    	pic[g_offset] = green[CLIP((y - rg))];
			pic[b_offset] = blue[CLIP((y + u1))];
			pic+=bpp;
		    }		// end test decode
		}		// end mx loop
		inl += nextinline;

		if (my >= cropy1) {
		    /* are we in a decode surface move the output pointer */
//		    pic += (nextoutline);
		}

	    }			// end my loop
	myframe->scanlength = (long) (softwidth * softheight * bpp);
	}
	break;
   case VIDEO_PALETTE_YUV420P:
	{			/* Not yet implemented */
	    for (my = 0; my < height; my +=2) {
		for (mx = 0; mx < width; mx += 2) {
		    /* test if we need to decode */
		    if ((my >= cropy1)
			&& (my < height - cropy2)
			&& (mx >= cropx1)
			&& (mx < width - cropx2)) {
			*pic++ = buf[inl+mx*2+0];
			*U++=buf[inl+mx*2+1];
			*pic++ = buf[inl+mx*2+2];
			*V++=buf[inl+mx*2+3];
			*pic1++ = buf[inl1+mx*2+0];
			*pic1++ = buf[inl1+mx*2+2];
			
		    }		// end test decode
		}		// end mx loop
		inl += (nextinline << 1);
		inl1 += (nextinline << 1);
		if (my >= cropy1) {
		    /* are we in a decode surface move the output pointer */
		    pic += (nextoutline);
		    pic1 += (nextoutline);
		}

	    }			// end my loop

	
	myframe->scanlength = (long) ((softwidth * softheight * 3) >> 1);
	}
	break;
    default:
	break;
  }				// end case
   return 0;
}				// end yuyv_translate
 
/* this function restore the missing header for the jpeg camera */
/* adapted from Till Adam create_jpeg_from_data() */
static int make_jpeg(struct spca50x_frame *myframe)
{
    __u8 *start;
    int i;
    __u8 value;
    int width = myframe->hdrwidth;
    int height = myframe->hdrheight;
    long inputsize = myframe->scanlength;
    __u8 *buf = myframe->tmpbuffer;
    __u8 *dst = myframe->data;
    start = dst;
    /* set up the default header */
    memcpy(dst, JPEGHeader, JPEGHEADER_LENGTH);
    /* setup quantization table */
    *(dst + 6) = 0;
    memcpy(dst + 7, myframe->decoder->quant[0], 64);
    *(dst + 7 + 64) = 1;
    memcpy(dst + 8 + 64, myframe->decoder->quant[1], 64);

    *(dst + 564) = width & 0xFF;	//Image width low byte
    *(dst + 563) = width >> 8 & 0xFF;	//Image width high byte
    *(dst + 562) = height & 0xFF;	//Image height low byte
    *(dst + 561) = height >> 8 & 0xFF;	//Image height high byte
    /* set the format */
    if (myframe->cameratype == JPEG) {
	*(dst + 567) = 0x22;
	dst += JPEGHEADER_LENGTH;
	for (i = 0; i < inputsize; i++) {
	    value = *(buf + i) & 0xFF;
	    *dst = value;
	    dst++;
	    if (value == 0xFF) {
		*dst = 0;
		dst++;
	    }
	}
    } else {
	*(dst + 567) = 0x21;
	dst += JPEGHEADER_LENGTH;
	memcpy(dst, buf, inputsize);
	dst += inputsize;
    }
    /* Add end of image marker */
    *(dst++) = 0xFF;
    *(dst++) = 0xD9;
    myframe->scanlength = (long) (dst - start);
    return 0;
}

static int make_jpeg_conexant(struct spca50x_frame *myframe)
{

    __u8 *buf = myframe->tmpbuffer;
    __u8 *dst = myframe->data;

    memcpy(dst, JPEGHeader, JPEGHEADER_LENGTH - 33);
    *(dst + 6) = 0;
    memcpy(dst + 7, myframe->decoder->quant[0], 64);
    *(dst + 7 + 64) = 1;
    memcpy(dst + 8 + 64, myframe->decoder->quant[1], 64);
    dst += (JPEGHEADER_LENGTH - 33);
    memcpy(dst, buf, myframe->scanlength);
    myframe->scanlength += (JPEGHEADER_LENGTH - 33);
    return 0;
}

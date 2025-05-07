# Copyright (c) 2025 Ashengut
# MIT License

import os
import re
import json
import random
from playsound import playsound
import tkinter as tk
from tkinter import filedialog
import threading
from datetime import datetime, timezone
import getpass
import subprocess
from pathlib import Path
import keyboard
import platform
import subprocess
from threading import Thread

KEY_SIGNATURES = [
    "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9",
    "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9",
    "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9",
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9",
    "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9",
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9",
    "A", "A5", "A6", "A6/9", "A7", "A7(#9)", "A7(b5)", "A7(b9)", "A7sus4", 
    "A9", "A11", "A13", "Aadd9", "Aaug", "Ab", "Ab5", "Ab6", "Ab6/9", "Ab7", 
    "Ab7(#9)", "Ab7(b5)", "Ab7(b9)", "Ab7sus4", "Ab9", "Ab11", "Ab13", 
    "Abadd9", "Abaug", "Abdim", "Abdim7", "Abm", "Abm6", "Abm7", "Abm7(b5)", 
    "Abm9", "Abm11", "Abm13", "Abmaj7", "Abmaj9", "Abmaj11", "Abmaj13", 
    "Absus2", "Absus4", "Adim", "Adim7", "Am", "Am6", "Am7", "Am7(b5)", 
    "Am9", "Am11", "Am13", "Amaj7", "Amaj9", "Amaj11", "Amaj13", "Asus2", 
    "Asus4", "A#", "A#5", "A#6", "A#6/9", "A#7", "A#7(#9)", "A#7(b5)", 
    "A#7(b9)", "A#7sus4", "A#9", "A#11", "A#13", "A#add9", "A#aug", "A#dim", 
    "A#dim7", "A#m", "A#m6", "A#m7", "A#m7(b5)", "A#m9", "A#m11", "A#m13", 
    "A#maj7", "A#maj9", "A#maj11", "A#maj13", "A#sus2", "A#sus4", "B", "B5", 
    "B6", "B6/9", "B7", "B7(#9)", "B7(b5)", "B7(b9)", "B7sus4", "B9", "B11", 
    "B13", "Badd9", "Baug", "Bb", "Bb5", "Bb6", "Bb6/9", "Bb7", "Bb7(#9)", 
    "Bb7(b5)", "Bb7(b9)", "Bb7sus4", "Bb9", "Bb11", "Bb13", "Bbadd9", 
    "Bbaug", "Bbdim", "Bbdim7", "Bbm", "Bbm6", "Bbm7", "Bbm7(b5)", "Bbm9", 
    "Bbm11", "Bbm13", "Bbmaj7", "Bbmaj9", "Bbmaj11", "Bbmaj13", "Bbsus2", 
    "Bbsus4", "Bdim", "Bdim7", "Bm", "Bm6", "Bm7", "Bm7(b5)", "Bm9", "Bm11", 
    "Bm13", "Bmaj7", "Bmaj9", "Bmaj11", "Bmaj13", "Bsus2", "Bsus4", "B#", 
    "B#5", "B#6", "B#6/9", "B#7", "B#7(#9)", "B#7(b5)", "B#7(b9)", "B#7sus4", 
    "B#9", "B#11", "B#13", "B#add9", "B#aug", "B#dim", "B#dim7", "B#m", 
    "B#m6", "B#m7", "B#m7(b5)", "B#m9", "B#m11", "B#m13", "B#maj7", "B#maj9", 
    "B#maj11", "B#maj13", "B#sus2", "B#sus4", "C", "C5", "C6", "C6/9", "C7", 
    "C7(#9)", "C7(b5)", "C7(b9)", "C7sus4", "C9", "C11", "C13", "Cadd9", 
    "Caug", "Cb", "Cb5", "Cb6", "Cb6/9", "Cb7", "Cb7(#9)", "Cb7(b5)", 
    "Cb7(b9)", "Cb7sus4", "Cb9", "Cb11", "Cb13", "Cbadd9", "Cbaug", "Cbdim", 
    "Cbdim7", "Cbm", "Cbm6", "Cbm7", "Cbm7(b5)", "Cbm9", "Cbm11", "Cbm13", 
    "Cbmaj7", "Cbmaj9", "Cbmaj11", "Cbmaj13", "Cbsus2", "Cbsus4", "Cdim", 
    "Cdim7", "Cm", "Cm6", "Cm7", "Cm7(b5)", "Cm9", "Cm11", "Cm13", "Cmaj7", 
    "Cmaj9", "Cmaj11", "Cmaj13", "Csus2", "Csus4", "C#", "C#5", "C#6", 
    "C#6/9", "C#7", "C#7(#9)", "C#7(b5)", "C#7(b9)", "C#7sus4", "C#9", 
    "C#11", "C#13", "C#add9", "C#aug", "C#dim", "C#dim7", "C#m", "C#m6", 
    "C#m7", "C#m7(b5)", "C#m9", "C#m11", "C#m13", "C#maj7", "C#maj9", 
    "C#maj11", "C#maj13", "C#sus2", "C#sus4", "D", "D5", "D6", "D6/9", "D7", 
    "D7(#9)", "D7(b5)", "D7(b9)", "D7sus4", "D9", "D11", "D13", "Dadd9", 
    "Daug", "Db", "Db5", "Db6", "Db6/9", "Db7", "Db7(#9)", "Db7(b5)", 
    "Db7(b9)", "Db7sus4", "Db9", "Db11", "Db13", "Dbadd9", "Dbaug", "Dbdim", 
    "Dbdim7", "Dbm", "Dbm6", "Dbm7", "Dbm7(b5)", "Dbm9", "Dbm11", "Dbm13", 
    "Dbmaj7", "Dbmaj9", "Dbmaj11", "Dbmaj13", "Dbsus2", "Dbsus4", "Ddim", 
    "Ddim7", "Dm", "Dm6", "Dm7", "Dm7(b5)", "Dm9", "Dm11", "Dm13", "Dmaj7", 
    "Dmaj9", "Dmaj11", "Dmaj13", "Dsus2", "Dsus4", "D#", "D#5", "D#6", 
    "D#6/9", "D#7", "D#7(#9)", "D#7(b5)", "D#7(b9)", "D#7sus4", "D#9", 
    "D#11", "D#13", "D#add9", "D#aug", "D#dim", "D#dim7", "D#m", "D#m6", 
    "D#m7", "D#m7(b5)", "D#m9", "D#m11", "D#m13", "D#maj7", "D#maj9", 
    "D#maj11", "D#maj13", "D#sus2", "D#sus4", "E", "E5", "E6", "E6/9", "E7", 
    "E7(#9)", "E7(b5)", "E7(b9)", "E7sus4", "E9", "E11", "E13", "Eadd9", 
    "Eaug", "Eb", "Eb5", "Eb6", "Eb6/9", "Eb7", "Eb7(#9)", "Eb7(b5)", 
    "Eb7(b9)", "Eb7sus4", "Eb9", "Eb11", "Eb13", "Ebadd9", "Ebaug", "Ebdim", 
    "Ebdim7", "Ebm", "Ebm6", "Ebm7", "Ebm7(b5)", "Ebm9", "Ebm11", "Ebm13", 
    "Ebmaj7", "Ebmaj9", "Ebmaj11", "Ebmaj13", "Ebsus2", "Ebsus4", "Edim", 
    "Edim7", "Em", "Em6", "Em7", "Em7(b5)", "Em9", "Em11", "Em13", "Emaj7", 
    "Emaj9", "Emaj11", "Emaj13", "Esus2", "Esus4", "E#", "E#5", "E#6", 
    "E#6/9", "E#7", "E#7(#9)", "E#7(b5)", "E#7(b9)", "E#7sus4", "E#9", 
    "E#11", "E#13", "E#add9", "E#aug", "E#dim", "E#dim7", "E#m", "E#m6", 
    "E#m7", "E#m7(b5)", "E#m9", "E#m11", "E#m13", "E#maj7", "E#maj9", 
    "E#maj11", "E#maj13", "E#sus2", "E#sus4", "F", "F5", "F6", "F6/9", "F7", 
    "F7(#9)", "F7(b5)", "F7(b9)", "F7sus4", "F9", "F11", "F13", "Fadd9",
    "Faug", "Fb", "Fb5", "Fb6", "Fb6/9", "Fb7", "Fb7(#9)", "Fb7(b5)", "Fb7(b9)", 
    "Fb7sus4", "Fb9", "Fb11", "Fb13", "Fbadd9", "Fbaug", "Fbdim", "Fbdim7", 
    "Fbm", "Fbm6", "Fbm7", "Fbm7(b5)", "Fbm9", "Fbm11", "Fbm13", "Fbmaj7", 
    "Fbmaj9", "Fbmaj11", "Fbmaj13", "Fbsus2", "Fbsus4", "Fdim", "Fdim7", 
    "Fm", "Fm6", "Fm7", "Fm7(b5)", "Fm9", "Fm11", "Fm13", "Fmaj7", "Fmaj9", 
    "Fmaj11", "Fmaj13", "Fsus2", "Fsus4", "F#", "F#5", "F#6", "F#6/9", "F#7", 
    "F#7(#9)", "F#7(b5)", "F#7(b9)", "F#7sus4", "F#9", "F#11", "F#13", 
    "F#add9", "F#aug", "F#dim", "F#dim7", "F#m", "F#m6", "F#m7", "F#m7(b5)", 
    "F#m9", "F#m11", "F#m13", "F#maj7", "F#maj9", "F#maj11", "F#maj13", 
    "F#sus2", "F#sus4", "G", "G5", "G6", "G6/9", "G7", "G7(#9)", "G7(b5)", 
    "G7(b9)", "G7sus4", "G9", "G11", "G13", "Gadd9", "Gaug", "Gb", "Gb5", 
    "Gb6", "Gb6/9", "Gb7", "Gb7(#9)", "Gb7(b5)", "Gb7(b9)", "Gb7sus4", "Gb9", 
    "Gb11", "Gb13", "Gbadd9", "Gbaug", "Gbdim", "Gbdim7", "Gbm", "Gbm6", 
    "Gbm7", "Gbm7(b5)", "Gbm9", "Gbm11", "Gbm13", "Gbmaj7", "Gbmaj9", 
    "Gbmaj11", "Gbmaj13", "Gbsus2", "Gbsus4", "Gdim", "Gdim7", "Gm", "Gm6", 
    "Gm7", "Gm7(b5)", "Gm9", "Gm11", "Gm13", "Gmaj7", "Gmaj9", "Gmaj11", 
    "Gmaj13", "Gsus2", "Gsus4", "G#", "G#5", "G#6", "G#6/9", "G#7", 
    "G#7(#9)", "G#7(b5)", "G#7(b9)", "G#7sus4", "G#9", "G#11", "G#13", 
    "G#add9", "G#aug", "G#dim", "G#dim7", "G#m", "G#m6", "G#m7", "G#m7(b5)", 
    "G#m9", "G#m11", "G#m13", "G#maj7", "G#maj9", "G#maj11", "G#maj13", 
    "G#sus2", "G#sus4", "Abmin", "Abmin6", "Abmin7", "Abmin7(b5)", "Abmin9", 
    "Abmin11", "Abmin13", "Adimin", "Ammin", "Ammin6", "Ammin7", "Ammin7(b5)", 
    "Ammin9", "Ammin11", "Ammin13", "A#min", "A#min6", "A#min7", "A#min7(b5)", 
    "A#min9", "A#min11", "A#min13", "Bmin", "Bmin6", "Bmin7", "Bmin7(b5)", 
    "Bmin9", "Bmin11", "Bmin13", "Bbmin", "Bbmin6", "Bbmin7", "Bbmin7(b5)", 
    "Bbmin9", "Bbmin11", "Bbmin13", "Cbmin", "Cbmin6", "Cbmin7", "Cbmin7(b5)", 
    "Cbmin9", "Cbmin11", "Cbmin13", "Cmin", "Cmin6", "Cmin7", "Cmin7(b5)", 
    "Cmin9", "Cmin11", "Cmin13", "C#min", "C#min6", "C#min7", "C#min7(b5)", 
    "C#min9", "C#min11", "C#min13", "Dbmin", "Dbmin6", "Dbmin7", "Dbmin7(b5)", 
    "Dbmin9", "Dbmin11", "Dbmin13", "Dmin", "Dmin6", "Dmin7", "Dmin7(b5)", 
    "Dmin9", "Dmin11", "Dmin13", "D#min", "D#min6", "D#min7", "D#min7(b5)", 
    "D#min9", "D#min11", "D#min13", "Emin", "Emin6", "Emin7", "Emin7(b5)", 
    "Emin9", "Emin11", "Emin13", "Ebmin", "Ebmin6", "Ebmin7", "Ebmin7(b5)", 
    "Ebmin9", "Ebmin11", "Ebmin13", "E#min", "E#min6", "E#min7", "E#min7(b5)", 
    "E#min9", "E#min11", "E#min13", "Fbmin", "Fbmin6", "Fbmin7", "Fbmin7(b5)", 
    "Fbmin9", "Fbmin11", "Fbmin13", "Fmin", "Fmin6", "Fmin7", "Fmin7(b5)", 
    "Fmin9", "Fmin11", "Fmin13", "F#min", "F#min6", "F#min7", "F#min7(b5)", 
    "F#min9", "F#min11", "F#min13", "Gbmin", "Gbmin6", "Gbmin7", "Gbmin7(b5)", 
    "Gbmin9", "Gbmin11", "Gbmin13", "Gmin", "Gmin6", "Gmin7", "Gmin7(b5)", 
    "Gmin9", "Gmin11", "Gmin13", "G#min", "G#min6", "G#min7", "G#min7(b5)", 
    "G#min9", "G#min11", "G#min13", "AB", "AB5", "AB6", "AB6/9", "AB7", 
    "AB7(#9)", "AB7(B5)", "AB7(B9)", "AB7sus4", "AB9", "AB11", "AB13", 
    "ABadd9", "ABaug", "ABdim", "ABdim7", "ABm", "ABm6", "ABm7", "ABm7(B5)", 
    "ABm9", "ABm11", "ABm13", "ABmaj7", "ABmaj9", "ABmaj11", "ABmaj13", 
    "ABsus2", "ABsus4", "BB", "BB5", "BB6", "BB6/9", "BB7", "BB7(#9)", 
    "BB7(B5)", "BB7(B9)", "BB7sus4", "BB9", "BB11", "BB13", "BBadd9", 
    "BBaug", "BBdim", "BBdim7", "BBm", "BBm6", "BBm7", "BBm7(B5)", "BBm9", 
    "BBm11", "BBm13", "BBmaj7", "BBmaj9", "BBmaj11", "BBmaj13", "BBsus2", 
    "BBsus4", "CB", "CB5", "CB6", "CB6/9", "CB7", "CB7(#9)", "CB7(B5)", 
    "CB7(B9)", "CB7sus4", "CB9", "CB11", "CB13", "CBadd9", "CBaug", "CBdim", 
    "CBdim7", "CBm", "CBm6", "CBm7", "CBm7(B5)", "CBm9", "CBm11", "CBm13", 
    "CBmaj7", "CBmaj9", "CBmaj11", "CBmaj13", "CBsus2", "CBsus4", "DB", 
    "DB5", "DB6", "DB6/9", "DB7", "DB7(#9)", "DB7(B5)", "DB7(B9)", "DB7sus4", 
    "DB9", "DB11", "DB13", "DBadd9", "DBaug", "DBdim", "DBdim7", "DBm", 
    "DBm6", "DBm7", "DBm7(B5)", "DBm9", "DBm11", "DBm13", "DBmaj7", "DBmaj9", 
    "DBmaj11", "DBmaj13", "DBsus2", "DBsus4", "EB", "EB5", "EB6", 
    "EB6/9", "EB7", "EB7(#9)", "EB7(B5)", "EB7(B9)", "EB7sus4", "EB9", 
    "EB11", "EB13", "EBadd9", "EBaug", "EBdim", "EBdim7", "EBm", "EBm6", 
    "EBm7", "EBm7(B5)", "EBm9", "EBm11", "EBm13", "EBmaj7", "EBmaj9", 
    "EBmaj11", "EBmaj13", "EBsus2", "EBsus4", "FB", "FB5", "FB6", "FB6/9", 
    "FB7", "FB7(#9)", "FB7(B5)", "FB7(B9)", "FB7sus4", "FB9", "FB11", 
    "FB13", "FBadd9", "FBaug", "FBdim", "FBdim7", "FBm", "FBm6", "FBm7", 
    "FBm7(B5)", "FBm9", "FBm11", "FBm13", "FBmaj7", "FBmaj9", "FBmaj11", 
    "FBmaj13", "FBsus2", "FBsus4", "GB", "GB5", "GB6", "GB6/9", "GB7", 
    "GB7(#9)", "GB7(B5)", "GB7(B9)", "GB7sus4", "GB9", "GB11", "GB13", 
    "GBadd9", "GBaug", "GBdim", "GBdim7", "GBm", "GBm6", "GBm7", "GBm7(B5)", 
    "GBm9", "GBm11", "GBm13", "GBmaj7", "GBmaj9", "GBmaj11", "GBmaj13", 
    "GBsus2", "GBsus4", "Ab7maj", "Ab9maj", "Ab11maj", "Ab13maj", "Ab7min", 
    "Ab6min", "Ab9min", "Ab11min", "Ab13min", "A7maj", "A9maj", "A11maj", 
    "A13maj", "A7min", "A6min", "A9min", "A11min", "A13min", "A#7maj", 
    "A#9maj", "A#11maj", "A#13maj", "A#7min", "A#6min", "A#9min", "A#11min", 
    "A#13min", "B7maj", "B9maj", "B11maj", "B13maj", "B7min", "B6min", 
    "B9min", "B11min", "B13min", "Bb7maj", "Bb9maj", "Bb11maj", "Bb13maj", 
    "Bb7min", "Bb6min", "Bb9min", "Bb11min", "Bb13min", "Cb7maj", "Cb9maj", 
    "Cb11maj", "Cb13maj", "Cb7min", "Cb6min", "Cb9min", "Cb11min", "Cb13min", 
    "C7maj", "C9maj", "C11maj", "C13maj", "C7min", "C6min", "C9min", 
    "C11min", "C13min", "C#7maj", "C#9maj", "C#11maj", "C#13maj", "C#7min", 
    "C#6min", "C#9min", "C#11min", "C#13min", "Db7maj", "Db9maj", "Db11maj", 
    "Db13maj", "Db7min", "Db6min", "Db9min", "Db11min", "Db13min", "D7maj", 
    "D9maj", "D11maj", "D13maj", "D7min", "D6min", "D9min", "D11min", 
    "D13min", "D#7maj", "D#9maj", "D#11maj", "D#13maj", "D#7min", "D#6min", 
    "D#9min", "D#11min", "D#13min", "E7maj", "E9maj", "E11maj", "E13maj", 
    "E7min", "E6min", "E9min", "E11min", "E13min", "Eb7maj", "Eb9maj", 
    "Eb11maj", "Eb13maj", "Eb7min", "Eb6min", "Eb9min", "Eb11min", "Eb13min", 
    "E#7maj", "E#9maj", "E#11maj", "E#13maj", "E#7min", "E#6min", "E#9min", 
    "E#11min", "E#13min", "Fb7maj", "Fb9maj", "Fb11maj", "Fb13maj", "Fb7min", 
    "Fb6min", "Fb9min", "Fb11min", "Fb13min", "F7maj", "F9maj", "F11maj", 
    "F13maj", "F7min", "F6min", "F9min", "F11min", "F13min", "F#7maj", 
    "F#9maj", "F#11maj", "F#13maj", "F#7min", "F#6min", "F#9min", "F#11min", 
    "F#13min", "Gb7maj", "Gb9maj", "Gb11maj", "Gb13maj", "Gb7min", "Gb6min", 
    "Gb9min", "Gb11min", "Gb13min", "G7maj", "G9maj", "G11maj", "G13maj", 
    "G7min", "G6min", "G9min", "G11min", "G13min", "G#7maj", "G#9maj", 
    "G#11maj", "G#13maj", "G#7min", "G#6min", "G#9min", "G#11min", 
    "G#13min", "AB7maj", "AB9maj", "AB11maj", "AB13maj", "AB7min", "AB6min", 
    "AB9min", "AB11min", "AB13min", "BB7maj", "BB9maj", "BB11maj", "BB13maj", 
    "BB7min", "BB6min", "BB9min", "BB11min", "BB13min", "CB7maj", "CB9maj", 
    "CB11maj", "CB13maj", "CB7min", "CB6min", "CB9min", "CB11min", 
    "CB13min", "DB7maj", "DB9maj", "DB11maj", "DB13maj", "DB7min", "DB6min", 
    "DB9min", "DB11min", "DB13min", "EB7maj", "EB9maj", "EB11maj", "EB13maj", 
    "EB7min", "EB6min", "EB9min", "EB11min", "EB13min", "FB7maj", "FB9maj", 
    "FB11maj", "FB13maj", "FB7min", "FB6min", "FB9min", "FB11min", "FB13min", 
    "GB7maj", "GB9maj", "GB11maj", "GB13maj", "GB7min", "GB6min", "GB9min", 
    "GB11min", "GB13min", "Ab7M", "Ab9M", "Ab11M", "Ab13M", "Ab7m", "Ab6m", 
    "Ab9m", "Ab11m", "Ab13m", "A7M", "A9M", "A11M", "A13M", "A7m", "A6m", 
    "A9m", "A11m", "A13m", "A#7M", "A#9M", "A#11M", "A#13M", "A#7m", "A#6m", 
    "A#9m", "A#11m", "A#13m", "B7M", "B9M", "B11M", "B13M", "B7m", "B6m", 
    "B9m", "B11m", "B13m", "Bb7M", "Bb9M", "Bb11M", "Bb13M", "Bb7m", "Bb6m", 
    "Bb9m", "Bb11m", "Bb13m", "Cb7M", "Cb9M", "Cb11M", "Cb13M", "Cb7m", 
    "Cb6m", "Cb9m", "Cb11m", "Cb13m", "C7M", "C9M", "C11M", "C13M", "C7m", 
    "C6m", "C9m", "C11m", "C13m", "C#7M", "C#9M", "C#11M", "C#13M", "C#7m", 
    "C#6m", "C#9m", "C#11m", "C#13m", "Db7M", "Db9M", "Db11M", "Db13M", 
    "Db7m", "Db6m", "Db9m", "Db11m", "Db13m", "D7M", "D9M", "D11M", "D13M", 
    "D7m", "D6m", "D9m", "D11m", "D13m", "D#7M", "D#9M", "D#11M", "D#13M", 
    "D#7m", "D#6m", "D#9m", "D#11m", "D#13m", "E7M", "E9M", "E11M", "E13M", 
    "E7m", "E6m", "E9m", "E11m", "E13m", "Eb7M", "Eb9M", "Eb11M", "Eb13M", 
    "Eb7m", "Eb6m", "Eb9m", "Eb11m", "Eb13m", "E#7M", "E#9M", "E#11M", 
    "E#13M", "E#7m", "E#6m", "E#9m", "E#11m", "E#13m", "Fb7M", "Fb9M", 
    "Fb11M", "Fb13M", "Fb7m", "Fb6m", "Fb9m", "Fb11m", "Fb13m", "F7M", 
    "F9M", "F11M", "F13M", "F7m", "F6m", "F9m", "F11m", "F13m", "F#7M", 
    "F#9M", "F#11M", "F#13M", "F#7m", "F#6m", "F#9m", "F#11m", "F#13m", 
    "Gb7M", "Gb9M", "Gb11M", "Gb13M", "Gb7m", "Gb6m", "Gb9m", "Gb11m", 
    "Gb13m", "G7M", "G9M", "G11M", "G13M", "G7m", "G6m", "G9m", "G11m", 
    "G13m", "G#7M", "G#9M", "G#11M", "G#13M", "G#7m", "G#6m", "G#9m", 
    "G#11m", "G#13m", "AB7M", "AB9M", "AB11M", "AB13M", "AB7m", "AB6m", 
    "AB9m", "AB11m", "AB13m", "BB7M", "BB9M", "BB11M", "BB13M", "BB7m", 
    "BB6m", "BB9m", "BB11m", "BB13m", "CB7M", "CB9M", "CB11M", "CB13M", 
    "CB7m", "CB6m", "CB9m", "CB11m", "CB13m", "DB7M", "DB9M", "DB11M", 
    "DB13M", "DB7m", "DB6m", "DB9m", "DB11m", "DB13m", "EB7M", "EB9M", 
    "EB11M", "EB13M", "EB7m", "EB6m", "EB9m", "EB11m", "EB13m", "FB7M", 
    "FB9M", "FB11M", "FB13M", "FB7m", "FB6m", "FB9m", "FB11m", "FB13m", 
    "GB7M", "GB9M", "GB11M", "GB13M", "GB7m", "GB6m", "GB9m", "GB11m", 
    "GB13m"
]
IGNORE_NUMBERS = {"909", "808", "707", "606", "505", "404", "303", "202", "101"}
HISTORY_LOG = "rename_history.json"

ASCII_ART = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠟⢋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⠁⣤⣐⠦⠀⢠⣶⣤⢭⡙⢿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠟⠁⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⢿⣿⣿⡿⠋⢱⣾⠃⠀⠀⠀⠉⠀⠀⠀⠈⠉⠐⣿⠘⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠃⠀⡀⢸⣿⠿⢛⣿⣿⣿⣿⣿⣿⣿⠿⢛⣫⣭⣶⣶⢂⣾⣿⣿⣿⣿⡷⡶⠉⠀⠀⠀⠀⢀⠀⠀⠀⠀⢀⣤⣾⣷⣤⡼⢿⣧⢻⣿⣿⣿
⣿⣿⣿⣿⡇⠀⠀⠄⠘⠁⠄⣾⣿⣿⣿⡿⢟⢉⣤⣾⣿⣿⣿⣿⡏⢸⣿⣿⡿⢛⡅⢀⡔⠁⠀⠀⠀⠐⠀⣠⣴⣶⠖⣩⡾⠿⠛⠋⠉⠀⠀⢈⣿⣿⣿
⣿⣿⣿⣿⡇⠀⠀⠂⠀⡖⡇⣿⣿⡿⢋⡴⠃⣾⣿⣿⣿⣿⠟⠉⣀⣈⡍⠉⣰⡿⠐⢻⠀⠀⠀⠀⠀⢂⠀⡰⠖⠊⠉⠁⣀⡀⠠⠄⢀⠀⣴⣿⣿⣿⣿
⣿⣿⣿⣿⣷⠐⠊⠁⠸⣿⣷⡘⢋⣴⡿⠃⠀⠛⠻⠟⠉⣠⣴⣿⣿⣿⡿⢱⠟⠃⠃⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠂⠀⠀⢀⣼⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣧⡀⠀⠀⠘⠟⠁⠌⠋⣠⣴⢟⣿⡆⠀⡏⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣷⣤⡀⢠⣾⣶⢀⣾⣿⣿⣾⣿⠁⣤⣥⣹⠿⠛⠁⠀⠀⢀⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡌⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢃⢾⡿⠁⣾⣿⣿⣿⣿⣿⠀⠉⠁⠀⠀⠀⠀⢀⠀⢾⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⡀⠀⠹⠜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠃⡼⣾⠁⠘⠿⠻⠿⠿⠟⠉⠀⠀⠀⠀⢀⣠⣾⣿⣷⡄⠹⣿⣿⣦⠀⠀⠀⠀⠀⠀⣠⢞⣼⣧⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠇⠀⠘⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣦⠈⠿⠛⢁⣀⣀⡀⠰⠞⣡⣾⣿⣿⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⡇⢠⣾⣿⣿⣿⣿⡆⢸⣿⣿⣿⡿⠀⡆⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⡿⠀⠾⢿⣿⣿⣿⣿⠇⣸⣿⣿⣿⠃⠀⠁⡥⠓⣬⠛⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣦⡄⠀⢠⣶⣶⡦⢄⠀⠀⠛⠇⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠋⠁⠀⠀⠀⠈⠉⠛⠛⠀⠉⠛⠉⠀⠀⠀⠀⣧⠙⠶⠘⢌⢻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣧⠀⠰⠿⠾⢿⣂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠶⢟⣨⠐⠂⠈⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠋⠀⠀⠀⠐⣮⡙⠣⣅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠵⢞⣃⠀⣿⣿⣿⣿⣿
⣿⣿⣿⠟⠀⠀⠀⠀⠄⣒⡲⠼⢷⠍⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡆⠀⠀⠀⠀⠀⢚⣋⡅⠀⣿⣿⣿⣿⣿
⣿⣿⠏⠀⠀⠀⠀⠀⠿⢫⣙⡻⠖⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⡇⠀⠀⠀⠀⠀⠨⠅⠀⢠⣿⣿⣿⣿⣿
⣿⣿⠀⠀⠀⠀⠀⠀⠠⠦⠉⠁⣠⣿⣿⣷⣶⣶⣤⣤⣀⣀⣀⣀⣀⠀⠀⢀⣀⣀⣀⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿
⣿⡯⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠘⠉⠻⠿⣿⣿⣿⣿
⣿⣷⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠧⠀⠀⠠⡀⠀⠄⣐⠂⠬⠽⠻⢿
⠟⠅⠀⠀⠀⠀⠀⠰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣷⣦⣤⣬⣤⣄⢢⣬⣭⣤⣽⣿
⣶⣶⣶⠀⣀⠂⢀⢑⣈⣙⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣾⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

"""

SPLASH_MESSAGES = [
    "Spoogner!",
    "When life gives you melonade...",
    "Reticent mollusk!",
    "Wherefore art thou, Saggy Man??!!",
    "¿Dónde está el baño en francés?",
    "Moist",
    "Protect your face when the bird",
    "(( #TOAD ))",
    "Unclog the frog",
    "Get boof'd!",
    "+3dB intersample peaking",
    "Free Willy, only not in public",
    "MY PECS HAVE PECS!!!",
    "100 push-ups, 100 sit-ups, 100 squats, and a 10-kilometer run – every single day!",
    "Pneu",
    "Press X to doubt commitment to Sparkle Motion",
    "To be fair, you have to have a very high IQ to understand Rick and Morty. The humour is extremely subtle, and without a solid grasp of theoretical physics most of the jokes will go over a typical viewer’s head. There’s also Rick’s nihilistic outlook, which is deftly woven into his characterisation- his personal philosophy draws heavily from Narodnaya Volya literature, for instance. The fans understand this stuff; they have the intellectual capacity to truly appreciate the depths of these jokes, to realise that they’re not just funny—they say something deep about LIFE. As a consequence people who dislike Rick & Morty truly ARE idiots- of course they wouldn’t appreciate, for instance, the humour in Rick’s existential catchphrase “Wubba Lubba Dub Dub,” which itself is a cryptic reference to Turgenev’s Russian epic Fathers and Sons. I’m smirking right now just imagining one of those addlepated simpletons scratching their heads in confusion as Dan Harmon’s genius wit unfolds itself on their television screens.",
    "Cockalorum!",
    "Snollygoster!",
    "Lickspittle!",
    "Smellfungus!",
    "Mumpsimus!",
    "Hobbledehoy!",
    "Pettifogger!",
    "Saltimbanque!",
    "Marin d’eau douce!",
    "Bachi-bouzouk!",
    "The absolute state of karaoke",
    "A wild Floridian appears",
    "Now 73% more funky fresh than the competition",
    "If this breaks, blame latency",
    "Dudn't do tax, but name thing real goode",
    "Warning: Can contains trace amounts of funk",
    "The military-industrial complex but simple so we can have fun too",
    "Politicians that know what is good art and what is bad art",
    "50 Senzu",
    "The ozone layer clenching real hard.",
    "Namaste, little grasshopper",
    "\"Whoa\"",
    "Behold, the Quantum Funkulator!",
    "Mom said it's my turn to rename samples!",
    "Twice the BPM, half the talent!",
    "Rename.exe has achieved sentience.",
    "The Stangle Spagner",
    "Tax the poor, feed the rich!",
    "Edmuntoni McMiloni",
    "Matt Damon!",
    "Chocolate pain",
    "Uncle Harlentoni Bentoni",
    "haha boobies",
    "Turtle Recall",
    "Donatellonicci",
    "Leonardolini",
    "Raphaeloni",
    "Michelangelonio",
    "Bortnite",
    "Shortnite: Tough day at the office"
]

KEY_MODIFIERS = [
    "minor", "major", "min", "maj", "Minor", "Major", "Min", "Maj"
]

LOG_RENAMED = "LOG_renamed.json"
LOG_PREVIEWS = "LOG_previews.json"
MAX_RENAME_HISTORY = 20  # For undo operations
MAX_PREVIEW_HISTORY = 100
CURRENT_USER = getpass.getuser()

def play_intro():
    def play_sound():
        try:
            play_sound_cross_platform(os.path.join("media", "turt.wav"))
        except Exception as e:
            print(f"Error: {e}")
    
    print(ASCII_ART)
    print("\n🐢 " + random.choice(SPLASH_MESSAGES) + "\n")
    
    # Play sound in background
    sound_thread = threading.Thread(target=play_sound)
    sound_thread.daemon = True
    sound_thread.start()

def sanitize_filename(filename):
    """Sanitize filenames by replacing spaces and special characters."""
    return filename.replace(" ", "_").replace("&", "").replace("'", "").lower()

def play_sound_threaded(sound_file):
    """Play sound in a separate thread to allow simultaneous playback."""
    try:
        play_sound_cross_platform(sound_file)  # Play sound (cross-platform)
    except Exception as e:
        print(f"Error playing sound: {e}")

def play_random_sound(sound_files):
    """Play a random sound from the list of preloaded `.wav` sound files."""
    try:
        if sound_files:
            sound_file = random.choice(sound_files)  # Select a random `.wav` file
            print(f"Playing: {os.path.basename(sound_file)}")
            play_sound_cross_platform(sound_file)  # Play the selected sound file
        else:
            print("No sound files found!")
    except Exception as e:
        print(f"Error playing sound: {e}")

def play_sound_cross_platform(file_path):
    """Cross-platform method to play a `.wav` file."""
    try:
        system = platform.system()
        if system == "Windows":
            # Use PowerShell to play sound on Windows
            subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{file_path}').PlaySync();"], check=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["afplay", file_path], check=True)
        elif system == "Linux":
            subprocess.run(["aplay", file_path], check=True)
        else:
            print(f"Unsupported platform: {system}. Cannot play sound.")
    except FileNotFoundError:
        print("Sound playback tool not found on this system. Ensure the required tool is installed.")
    except Exception as e:
        print(f"Error during sound playback: {e}")

def select_files_and_folders():
    """Use tkinter to select files and folders"""
    root = tk.Tk()
    root.withdraw()
    
    files = list(filedialog.askopenfilenames(
        title="Select files to rename",
        filetypes=[("Audio Files", "*.wav *.mp3 *.aif *.aiff"), ("All Files", "*.*")]
    ))
    
    folder = filedialog.askdirectory(title="Select folder (optional)")
    if folder:
        for root, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename.lower().endswith(('.wav', '.mp3', '.aif', '.aiff')):
                    files.append(os.path.join(root, filename))
    
    return files  

def run_remove_duplicates_script():
    script_dir = Path(__file__).parent.resolve()
    script_path = script_dir / "media" / "the_turtinator_0.0.5.py"
    if script_path.exists():
        subprocess.run(["python", str(script_path)])
    else:
        print(f"Script not found: {script_path}")

def rename_with_order(files, order_type, dry_run=True):
    """Rename files with specified ordering of key, BPM, and prefix."""
    results = []
    
    for file in files:
        dir_, fname = os.path.split(file)
        name, ext = os.path.splitext(fname)
        
        # Extract metadata
        key, bpm, _, _ = extract_metadata(name)
        prefix = name.split('_')[0]
        
        # Clean up the name
        cleaned_name = clean_redundant_modifiers(name, key, bpm)
        parts = [p for p in cleaned_name.split('_') if p]
        
        # Remove prefix, key, and BPM from parts
        parts = [p for p in parts if p != prefix and p != key and (not bpm or p != str(bpm))]
        
        # Order mapping
        orders = {
            1: ['KEY', 'BPM', 'PREFIX'],  # KEY -> BPM -> PREFIX
            2: ['KEY', 'PREFIX', 'BPM'],  # KEY -> PREFIX -> BPM
            3: ['BPM', 'KEY', 'PREFIX'],  # BPM -> KEY -> PREFIX
            4: ['BPM', 'PREFIX', 'KEY'],  # BPM -> PREFIX -> KEY
            5: ['PREFIX', 'KEY', 'BPM'],  # PREFIX -> KEY -> BPM
            6: ['PREFIX', 'BPM', 'KEY']   # PREFIX -> BPM -> KEY
        }
        
        # Create new name based on order
        new_parts = []
        components = {'KEY': key, 'BPM': str(bpm) if bpm else None, 'PREFIX': prefix}
        
        # Add components in the specified order
        for component in orders[order_type]:
            if components[component]:
                new_parts.append(components[component])
        
        # Add remaining parts
        new_parts.extend(parts)
        
        # Create new name
        new_name = '_'.join(filter(None, new_parts)) + ext
        new_path = os.path.join(dir_, new_name)
        
        if new_path != file:
            if not dry_run:
                try:
                    os.rename(file, new_path)
                    results.append({"old": file, "new": new_path})
                except Exception as e:
                    print(f"Error renaming {fname}: {e}")
            print(f"✅ {fname} ➜ {new_name}")
        else:
            print(f"🔸 {fname} unchanged (already in desired format)")
    
    return results

def log_operation(operation, is_preview=False):
    """Log rename operations with timestamp"""
    log_file = LOG_PREVIEWS if is_preview else LOG_RENAMED
    max_entries = MAX_PREVIEW_HISTORY if is_preview else MAX_RENAME_HISTORY
    
    try:
        with open(log_file, 'r') as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log = []
    
    # Add new operation
    log.append(operation)
    
    # Keep only the latest entries
    log = log[-max_entries:]
    
    with open(log_file, 'w') as f:
        json.dump(log, f, indent=2)

def undo_operation(index=None):
    """Undo rename operations, either last one or selected from history"""
    try:
        with open(LOG_RENAMED, 'r') as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("🚫 No rename history found.")
        return False
    
    if not log:
        print("🚫 No operations to undo.")
        return False
    
    if index is None:
        # Undo last operation
        operation = log.pop()
    else:
        # Undo specific operation
        if 0 <= index < len(log):
            operation = log.pop(index)
        else:
            print("🚫 Invalid operation index.")
            return False
    
    # Perform the undo
    for entry in reversed(operation['entries']):
        if os.path.exists(entry['new']):
            try:
                os.rename(entry['new'], entry['old'])
                print(f"↩️  {entry['new']} ➜ {entry['old']}")
            except Exception as e:
                print(f"Error undoing rename: {e}")
    
    # Save updated log
    with open(LOG_RENAMED, 'w') as f:
        json.dump(log, f, indent=2)
    return True

def find_files(path):
    if os.path.isfile(path):
        return [path]
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
    ]

def remove_redundant_numbers(name):
    """
    Detect and remove redundant sequences of repeating numbers.
    Handles both cases:
    1. Simple repeating numbers: "_5_5_5" → "_5"
    2. Numbers with leading zeros: "_05_5_5_5" → "_05"
    """
    # First, handle numbers with same value but different formatting (05 and 5)
    pattern = r'_(?:0*(\d+)_)+0*\1(?=_|$)'
    while re.search(pattern, name):
        name = re.sub(pattern, r'_\1', name)
    
    # Then handle any remaining consecutive identical numbers
    pattern = r'(_\d+)(?:\1)+(?=_|$)'
    while re.search(pattern, name):
        name = re.sub(pattern, r'\1', name)
    
    return name

def clean_redundant_modifiers(name, key, bpm=None):
    """
    Remove redundant key and modifier information from the filename.
    """
    cleaned_name = name
    
    if bpm:
        # Remove BPM suffix format and duplicates
        cleaned_name = re.sub(rf"{bpm}(?:BPM|bpm)", "", cleaned_name)
        # Remove all instances of BPM except the first one
        bpm_matches = list(re.finditer(rf"(?:^|_){bpm}(?=_|$)", cleaned_name))
        if len(bpm_matches) > 1:
            for match in reversed(bpm_matches[1:]):
                cleaned_name = cleaned_name[:match.start()] + cleaned_name[match.end():]

    if key:
        # Extract base note and check for extensions
        key_parts = re.match(r"([A-G]#?b?)((?:maj|min|Major|Minor|Maj|Min|m|M)(?:7|9|11|13)?)?", key)
        if key_parts:
            base_note = key_parts.group(1)
            modifier = key_parts.group(2) or ""
            
            # Create patterns to match key variations
            patterns = [
                rf"(?:^|_){re.escape(base_note + modifier)}(?:$|_)",
                rf"(?:^|_){re.escape(base_note)}[ _]?(?:maj|Maj|MAJ|min|Min|MIN|m)(?:$|_)",
                rf"(?:^|_){re.escape(base_note)}(?:$|_)"
            ]
            
            # Remove all instances except the first one
            for pattern in patterns:
                matches = list(re.finditer(pattern, cleaned_name, re.IGNORECASE))
                if len(matches) > 1:
                    for match in reversed(matches[1:]):
                        cleaned_name = cleaned_name[:match.start()] + cleaned_name[match.end():]

    # Clean up multiple underscores
    cleaned_name = re.sub(r'_+', '_', cleaned_name)
    return cleaned_name.strip('_')

def extract_metadata(filename):
    """
    Extract key, BPM, and other metadata from the filename.
    """
    parts = re.split(r"[ _\-]", filename)
    key = None
    bpm_candidates = []
    bpm = None
    bpm_tag_found = False
    
    # First check for BPM with suffix - now case insensitive
    bpm_with_suffix = re.search(r'(\d+)(?:BPM|bpm)', filename)
    if bpm_with_suffix:
        bpm = int(bpm_with_suffix.group(1))
        bpm_tag_found = True
    
    # Look for chord patterns including spaced versions
    # Enhanced pattern to catch "G# Min" format
    chord_pattern = r"([A-G]#?b?)[ _]?(?:maj|Maj|MAJ|min|Min|MIN|m)?\d*"
    spaced_minor_pattern = r"([A-G]#?b?)[ _](?:min|Min|MIN)\b"
    
    # First try to find spaced minor pattern
    spaced_minor_match = re.search(spaced_minor_pattern, filename)
    if spaced_minor_match:
        key = f"{spaced_minor_match.group(1)}m"
    else:
        # Search in the full filename for complete chord patterns
        full_chord_match = re.search(rf"(?:^|_)({chord_pattern})(?:$|_)", filename)
        if full_chord_match:
            chord = full_chord_match.group(1).replace(" ", "")
            # If it's a major chord without extension, just use the base note
            if re.search(r"(?i)maj", chord) and not re.search(r"\d+$", chord):
                key = re.match(r"([A-G]#?b?)", chord).group(1)
            # Keep minor notation
            elif re.search(r"(?i)min|m$", chord):
                base_note = re.match(r"([A-G]#?b?)", chord).group(1)
                key = f"{base_note}m"
            # For other cases, keep as is
            else:
                key = chord
    
    # If no key found yet, check individual parts
    if not key:
        for part in parts:
            if re.match(rf"^{chord_pattern}$", part):
                chord = part.replace(" ", "")
                if re.search(r"(?i)maj", chord) and not re.search(r"\d+$", chord):
                    key = re.match(r"([A-G]#?b?)", chord).group(1)
                elif re.search(r"(?i)min|m$", chord):
                    base_note = re.match(r"([A-G]#?b?)", chord).group(1)
                    key = f"{base_note}m"
                else:
                    key = chord
                break

    # Detect BPM values
    numbers = re.findall(r'\d+', filename)
    for num in numbers:
        if num not in IGNORE_NUMBERS:
            num = int(num)
            if num > 40:  # Likely a BPM if above 40
                if not bpm or num > bpm:
                    bpm = num
            bpm_candidates.append(num)

    # Calculate extra (smallest number not chosen as BPM)
    extra = None
    if bpm_candidates:
        non_bpm_numbers = [n for n in bpm_candidates if n != bpm]
        if non_bpm_numbers:
            extra = min(non_bpm_numbers)

    return key, bpm, bpm_tag_found, extra

def sanitize_name(name):
    """
    Replace multiple underscores, dashes, or spaces with a single underscore and remove trailing underscores.
    """
    name = re.sub(r"[ _-]+", "_", name)  # Collapse multiple separators into a single underscore
    return name.strip("_")

def rename_file(path, dry_run=False, history=None):
    """
    Rename a file based on extracted metadata and sanitization rules.
    """
    dir_, fname = os.path.split(path)
    name, ext = os.path.splitext(fname)

    # Extract metadata
    key, bpm, bpm_tag_found, extra = extract_metadata(name)

    # First clean up the name
    cleaned_name = clean_redundant_modifiers(name, key, bpm)

    # Split into parts and filter out empty parts
    parts = [p for p in cleaned_name.split('_') if p]
    
    # Initialize new parts list
    new_parts = []
    
    # Add base (first part)
    if parts:
        new_parts.append(parts[0])
        parts = parts[1:]
    
    # Add key if exists (using the simplified version)
    if key:
        # Convert minor notation to 'm' format
        if re.search(r'(?i)min$', key):
            key = re.sub(r'(?i)min$', 'm', key)
        # Remove major notation completely
        elif re.search(r'(?i)maj$', key):
            key = re.sub(r'(?i)maj$', '', key)
        new_parts.append(key)
    
    # Add BPM if exists
    if bpm:
        new_parts.append(str(bpm))
    
    # Add remaining parts, excluding duplicates and cleaned up
    seen = set(new_parts)
    for part in parts:
        # Skip if it's a duplicate of key or BPM
        if (key and part == key) or (bpm and part == str(bpm)):
            continue
            
        # Special handling for parts containing the key
        if key:
            base_note = re.match(r"([A-G]#?b?)", key).group(1)
            if re.search(rf"^{base_note}(?:maj|min|Maj|Min|m|M)?$", part, re.IGNORECASE):
                continue
        
        if part not in seen:
            new_parts.append(part)
            seen.add(part)

    # Join parts and create new name
    new_name = '_'.join(new_parts) + ext
    new_path = os.path.join(dir_, new_name)

    # Rename if needed
    if new_path != path:
        if not dry_run:
            os.rename(path, new_path)
            if history is not None:
                history.append({"old": path, "new": new_path})
        print(f"✅ {fname} ➜ {new_name}")
    else:
        print(f"🔸 {fname} unchanged")

def undo_all():
    """
    Undo all renaming operations by referring to the history log.
    """
    if not os.path.exists(LOG_RENAMED):
        print("🚫 No rename history found.")
        return
    
    with open(LOG_RENAMED, "r") as f:
        history = json.load(f)
        for entry in reversed(history):
            if os.path.exists(entry["new"]):
                try:
                 os.rename(entry["new"], entry["old"])
                 print(f"↩️  {entry['new']} ➜ {entry['old']}")
                except Exception as e:
                 print(f"Error undoing {entry['new']}: {e}")

    # Remove the log after undoing all operations
    os.remove(LOG_RENAMED)

def preload_sound_files(media_dir="media"):
    """Preload all `.wav` sound files (except `turt.wav`) from the media directory and subdirectories."""
    sound_files = []
    for root, _, files in os.walk(media_dir):
        for file in files:
            if file.lower().endswith(".wav") and file != "turt.wav":
                sound_files.append(os.path.join(root, file))
    return sound_files

def the_salad_bar(sound_files):
    """The Salad Bar™️: Wait for spacebar press to play a random sound."""
    print("\n🎵 The Salad Bar™️: Press [Space] to play a random sound, or [Esc] to return to the menu.")
    print("Listening for key presses...")

    while True:
        event = keyboard.read_event()
        if event.event_type == "down":
            if event.name == "space":
                sound_file = random.choice(sound_files)  # Pick a random sound
                print(f"Playing: {os.path.basename(sound_file)}")
                # Use a thread to play the sound
                Thread(target=play_sound_threaded, args=(sound_file,)).start()
            elif event.name == "esc":
                print("\nReturning to the main menu...")
                break

def show_menu(preloaded_sound_files):
    """Display the main menu and handle user interaction."""
    menu_options = {
        1: "Batch prefix",
        2: "Batch prefix (Dry run)",
        3: "Batch rename",
        4: "Batch rename (Dry run)",
        5: "Undo last",
        6: "Undo (Select)",
        7: "Turtle Recall (Undo all)",
        8: "Clean file name gooder this time (subjective)",
        9: "The Salad Bar™️: No calorie sound bites",
        10: "Exit"
    }

    while True:
        print("\nMain Menu:")
        for key, value in menu_options.items():
            print(f"[{key}] {value}")
        
        try:
            choice = int(input("\nEnter your choice (1-10): "))
            if choice == 9:
                the_salad_bar(preloaded_sound_files)
            elif choice == 10:
                return choice  # Exit
            elif choice in menu_options:
                return choice
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Invalid input, please enter a number between 1 and 10.")

def show_ordering_options():
    print("\nSelect ordering:")
    print("[1] KEY -> BPM -> PREFIX")
    print("[2] KEY -> PREFIX -> BPM")
    print("[3] BPM -> KEY -> PREFIX")
    print("[4] BPM -> PREFIX -> KEY")
    print("[5] PREFIX -> KEY -> BPM")
    print("[6] PREFIX -> BPM -> KEY")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
        except ValueError:
            pass
        print("Invalid choice, please try again.")

def main():
    play_intro()
    
    # Preload `.wav` sound files
    preloaded_sound_files = preload_sound_files()
    if not preloaded_sound_files:
        print("⚠️ Warning: No sound files found in the 'media' folder. The Salad Bar™️ will be unavailable.")
    
    while True:
        choice = show_menu(preloaded_sound_files)  # Pass preloaded sound files
        
        if choice == 9:
            the_salad_bar(preloaded_sound_files)
        elif choice == 10:
            print("\nGoodbye! 🐢")
            break
        elif choice == 8:
            run_remove_duplicates_script()
            play_random_sound(preloaded_sound_files)  # Play random sound on success
            input("\nPress Enter to continue...")
        elif choice in [1, 2]:  # Batch prefix options
            try:
                import batch_prefixer
                if batch_prefixer.main(dry_run=(choice == 2)):
                    play_random_sound(preloaded_sound_files)  # Play random sound on success
            except Exception as e:
                print(f"Error running batch prefixer: {e}")
        elif choice in [3, 4]:  # Batch rename options
            files = select_files_and_folders()
            if not files:
                print("No files selected.")
                continue
            
            order_type = show_ordering_options()
            dry_run = (choice == 4)  # Dry run if choice is 4
            results = rename_with_order(files, order_type, dry_run=dry_run)
            
            if results and not dry_run:
                operation = {
                    'entries': results,
                    'order_type': order_type,
                    'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'user': CURRENT_USER
                }
                log_operation(operation, is_preview=False)
                play_random_sound(preloaded_sound_files)  # Play random sound on success
        elif choice == 5:  # Undo last
            if undo_operation():
                play_random_sound(preloaded_sound_files)  # Play random sound on success
        elif choice == 6:  # Undo select
            try:
                with open(LOG_RENAMED, 'r') as f:
                    log = json.load(f)
                
                print("\nSelect operation to undo:")
                for i, op in enumerate(log):
                    timestamp = op['timestamp']
                    num_files = len(op['entries'])
                    print(f"[{i+1}] {timestamp} - {num_files} files")
                
                idx = int(input("\nEnter number (1-%d): " % len(log))) - 1
                undo_operation(idx)
                play_random_sound(preloaded_sound_files)  # Play random sound on success
            except (FileNotFoundError, json.JSONDecodeError):
                print("🚫 No rename history found.")
        elif choice == 7:  # Undo all
            try:
                with open(LOG_RENAMED, 'r') as f:
                    log = json.load(f)
                
                for _ in range(len(log)):
                    undo_operation()
                
                # Clear the log and add the divorce message
                with open(LOG_RENAMED, 'w') as f:
                    f.write("Consider that a divorce")
                play_random_sound(preloaded_sound_files)  # Play random sound on success
            except (FileNotFoundError, json.JSONDecodeError):
                print("🚫 No rename history found.")
        
        input("\nPress Enter to continue...")
        

if __name__ == "__main__":
    main()

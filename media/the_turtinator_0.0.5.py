# Copyright (c) 2025 Ashengut
# MIT License

import os
import re
import random
from pathlib import Path
import sys

try:
    from playsound import playsound
except ImportError:
    print("playsound not installed. Please run: pip install playsound")
    sys.exit(1)

VALID_KEYS = [
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

MAJOR_WORDS = {"Maj", "maj", "Major", "major"}
MINOR_WORDS = {"Min", "min", "Minor", "minor"}

def normalize_minor(key):
    return key + "m"

def normalize_key_and_mode(parts):
    new_parts = []
    idx = 0
    used_keys = set()
    while idx < len(parts):
        part = parts[idx]
        key_match = None
        for key in VALID_KEYS:
            if part == key:
                key_match = key
                break
        if key_match and idx + 1 < len(parts):
            next_part = parts[idx + 1]
            if next_part in MINOR_WORDS:
                key_token = normalize_minor(key_match)
                if key_token not in used_keys:
                    new_parts.append(key_token)
                    used_keys.add(key_token)
                idx += 2
                continue
            elif next_part in MAJOR_WORDS:
                if key_match not in used_keys:
                    new_parts.append(key_match)
                    used_keys.add(key_match)
                idx += 2
                continue
        min_match = re.match(rf"^({'|'.join(map(re.escape, VALID_KEYS))})(?:_| )?({'|'.join(MINOR_WORDS)})$", part, re.IGNORECASE)
        if min_match:
            key_token = normalize_minor(min_match.group(1))
            if key_token not in used_keys:
                new_parts.append(key_token)
                used_keys.add(key_token)
            idx += 1
            continue
        if key_match and part not in used_keys:
            new_parts.append(part)
            used_keys.add(part)
            idx += 1
            continue
        if part in MAJOR_WORDS or part in MINOR_WORDS:
            idx += 1
            continue
        new_parts.append(part)
        idx += 1
    return new_parts

def clean_filename(filename):
    name, ext = os.path.splitext(filename)
    name = re.sub(r'[_\-\s/]+', '_', name)
    raw_parts = name.split('_')
    parts = normalize_key_and_mode(raw_parts)
    found_key = None
    found_bpm = None
    new_parts = []
    used_keys = set()
    used_bpm = set()
    for part in parts:
        if not found_key:
            if part in VALID_KEYS or (part.endswith('m') and part[:-1] in VALID_KEYS):
                found_key = part
                new_parts.append(part)
                used_keys.add(part)
                continue
        if not found_bpm and part.isdigit() and 40 <= int(part) <= 300:
            found_bpm = part
            new_parts.append(part)
            used_bpm.add(part)
            continue
        if (part in VALID_KEYS or (part.endswith('m') and part[:-1] in VALID_KEYS)) and part in used_keys:
            continue
        if part.isdigit() and part in used_bpm:
            continue
        new_parts.append(part)
    new_name = '_'.join(filter(None, new_parts))
    new_name = re.sub(r'[_\-\s/]+', '_', new_name)
    new_name = new_name.strip('_- /.')
    return new_name + ext

def play_random_sound(media_folder="media"):
    sounds = [
        str(f) for f in Path(media_folder).glob("*")
        if f.is_file() and f.suffix.lower() in (".wav", ".mp3", ".ogg") and f.name != "turt.wav"
    ]
    if sounds:
        chosen = random.choice(sounds)
        try:
            playsound(chosen)
        except Exception as e:
            print(f"Could not play sound {chosen}: {e}")

def clean_directory_recursive(directory):
    changes_made = False
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.wav', '.mp3', '.aif', '.aiff', '.ogg')):
                old_path = Path(root) / filename
                new_name = clean_filename(filename)
                if new_name != filename:
                    new_path = Path(root) / new_name
                    try:
                        old_path.rename(new_path)
                        print(f"✅ {filename} ➜ {new_name}")
                        changes_made = True
                    except Exception as e:
                        print(f"Error renaming {filename}: {e}")
    if not changes_made:
        print("No duplicate BPMs, keys, or mode words found to clean up.")

def main():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory(title="Select root folder with audio files")
    except:
        directory = input("\nEnter the full path to the root folder with audio files: ")
    if directory and os.path.isdir(directory):
        clean_directory_recursive(directory)
        play_random_sound("media")
        input("\nPress Enter to exit...")
    else:
        print("Invalid directory path!")
        play_random_sound("media")

if __name__ == "__main__":
    main()
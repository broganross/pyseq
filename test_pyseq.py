
import os
import sys
from unittest import TestCase

import pyseq
from pyseq import Item
from pyseq import Sequence
from pyseq import SequenceError


class ItemTestCase(TestCase):

    def test_init(self):
        i = Item("")
        self.assertEqual(i.item, "")
        self.assertEqual(i._Item__path, os.getcwd())
        self.assertEqual(i._Item__dirname, "")
        self.assertEqual(i._Item__filename, "")
        self.assertEqual(i._Item__digits, [])
        self.assertEqual(i._Item__parts, [""])
        self.assertEqual(i.frame, "")
        self.assertEqual(i.head, "")
        self.assertEqual(i.tail, "")

        i = Item("something")
        self.assertEqual(i.item, "something")
        self.assertEqual(i._Item__path, os.path.join(os.getcwd(), "something"))
        self.assertEqual(i._Item__dirname, "")
        self.assertEqual(i._Item__filename, "something")
        self.assertEqual(i._Item__digits, [])
        self.assertEqual(i._Item__parts, ["something"])
        self.assertEqual(i.frame, "")
        self.assertEqual(i.head, "something")
        self.assertEqual(i.tail, "")

        i = Item("s0m3th1ng_else")
        self.assertEqual(i.item, "s0m3th1ng_else")
        self.assertEqual(i._Item__path, os.path.join(os.getcwd(), "s0m3th1ng_else"))
        self.assertEqual(i._Item__dirname, "")
        self.assertEqual(i._Item__filename, "s0m3th1ng_else")
        self.assertEqual(i._Item__digits, ["0", "3", "1"])
        self.assertEqual(i._Item__parts, ["s", "m", "th", "ng_else"])
        self.assertEqual(i.frame, "")
        self.assertEqual(i.head, "s0m3th1ng_else")
        self.assertEqual(i.tail, "")

        root = "/root"
        if sys.platform.startswith("win"):
            root = "c:\\"
        path = os.path.join(root, "something", "else", "filename.txt")
        i = Item(path)
        self.assertEqual(i.item, path)
        self.assertEqual(i._Item__path, path)
        self.assertEqual(i._Item__dirname, os.path.dirname(path))
        self.assertEqual(i._Item__filename, os.path.basename(path))
        self.assertEqual(i._Item__digits, [])
        self.assertEqual(i._Item__parts, ["filename.txt"])
        self.assertEqual(i.frame, "")
        self.assertEqual(i.head, "filename.txt")
        self.assertEqual(i.tail, "")

        path = os.path.join(root, "filename.005.ext")
        i = Item(path)
        self.assertEqual(i.item, path)
        self.assertEqual(i._Item__path, path)
        self.assertEqual(i._Item__dirname, os.path.dirname(path))
        self.assertEqual(i._Item__filename, os.path.basename(path))
        self.assertEqual(i._Item__digits, ["005"])
        self.assertEqual(i._Item__parts, ["filename.", ".ext"])
        self.assertEqual(i.frame, "")
        self.assertEqual(i.head, "filename.005.ext")
        self.assertEqual(i.tail, "")

    def test_path_prop(self):
        root = "/root"
        if sys.platform.startswith("win"):
            root = "c:\\"
        ps = [("something", os.path.join(os.getcwd(), "something")),
              ("else.001.ext", os.path.join(os.getcwd(), "else.001.ext")),
              (os.path.join(root, "thing", "file.txt"), os.path.join(root, "thing", "file.txt"))
              ]

        for p, a in ps:
            i = Item(p)
            self.assertEqual(i.path, a)

    def test_name_prop(self):
        root = "/root"
        if sys.platform.startswith("win"):
            root = "c:\\"
        ps = [("something", "something"),
              ("else.001.ext", "else.001.ext"),
              (os.path.join(root, "thing", "file.txt"), "file.txt")
              ]

        for p, a in ps:
            i = Item(p)
            self.assertEqual(i.name, a)

    def test_dirname_prop(self):
        root = "/root"
        if sys.platform.startswith("win"):
            root = "c:\\"
        ps = [("something", ""),
              ("else.001.ext", ""),
              (os.path.join(root, "thing", "file.txt"), os.path.join(root, "thing"))
              ]

        for p, a in ps:
            i = Item(p)
            self.assertEqual(i.dirname, a)

    def test_digits_prop(self):
        root = "/root"
        if sys.platform.startswith("win"):
            root = "c:\\"
        ps = [("something", []),
              ("else.001.ext", ["001"]),
              (os.path.join(root, "thing", "f1l3.txt"), ["1", "3"])
              ]

        for p, a in ps:
            i = Item(p)
            self.assertEqual(i.digits, a)

    def test_parts_prop(self):
        root = "/root"
        if sys.platform.startswith("win"):
            root = "c:\\"
        ps = [("something", ["something"]),
              ("else.001.ext", ["else.", ".ext"]),
              (os.path.join(root, "thing", "f1l3.txt"), ["f", "l", ".txt"])
              ]

        for p, a in ps:
            i = Item(p)
            self.assertEqual(i.parts, a)

    def test_signature_prop(self):
        root = "/root"
        if sys.platform.startswith("win"):
            root = "c:\\"
        ps = [("something", "something"),
              ("else.001.ext", "else..ext"),
              (os.path.join(root, "thing", "f1l3.txt"), "fl.txt")
              ]

        for p, a in ps:
            i = Item(p)
            self.assertEqual(i.signature, a)

    def test_isSibling(self):
        ps = [("else.001.ext", "else.002.ext", True),
              ("some.1.ext", "some.4.ext", True),
              ("fname.ext", "fname2.ext", False)]
        for p in ps:
            i = Item(p[0])
            c = p[1]
            self.assertEqual(i.isSibling(c), p[2])

    def test_isSibling_prop_updates(self):
        ps = [("else.12.ext", "else.23.ext", True, "12", "else.", ".ext"),
              ("fname.1.ext", "fname21.ext", False, "", "fname.1.ext", ""),
              ("fname.12.ext", "fname.1.ext", True, "12", "fname.", ".ext"),
              ("a.2020.ext", "b.2121.ext", False, "", "a.2020.ext", ""),
              ("fname01.005.ext", "fname03.001.ext", False, "", "fname01.005.ext", "")]
        for p in ps:
            i = Item(p[0])
            c = p[1]
            self.assertEqual(i.isSibling(c), p[2])
            self.assertEqual(i.frame, p[3])
            self.assertEqual(i.head, p[4])
            self.assertEqual(i.tail, p[5])


class TestSequence(TestCase):
    def test_init(self):
        self.assertRaises(TypeError, Sequence)
        i = Item("fname.001.ext")
        s = Sequence([i])
        self.assertEqual(len(s), 1)
        i0 = Item("fname02.002.ext")
        i1 = Item("fname03.001.ext")
        s = Sequence([i0, i1])
        self.assertEqual(len(s), 1)
        i1 = Item("fname02.012.ext")
        s = Sequence([i0, i1])
        self.assertEqual(len(s), 2)

    def test_attr(self):
        s = Sequence(["fname01.ext", "fname03.ext"])
        atts = s.__attrs__()
        self.assertEqual(atts["l"], 2)
        self.assertEqual(atts["s"], 1)
        self.assertEqual(atts['e'], 3)
        self.assertEqual(atts['f'], [1, 3])
        self.assertEqual(atts['m'], [2])
        self.assertEqual(atts['p'], "%02d")
        self.assertEqual(atts['r'], "1-3")
        self.assertEqual(atts['R'], "1 3")
        self.assertEqual(atts['h'], "fname")
        self.assertEqual(atts['t'], ".ext")

    def test_str(self):
        s = Sequence(["fname01.ext"])
        self.assertEqual(str(s), "fname01.ext")
        s = Sequence(["fname02.ext", "fname12.ext"])
        self.assertEqual(str(s), "fname2-12.ext")

    def test_format(self):
        s = Sequence(["fname.001.ext", "fname.003.ext", "fname.004.ext"])
        self.assertEqual(s.format(), "   3 fname.%03d.ext 1 3-4")
        ats = s.__attrs__()
        for k, v in ats.items():
            self.assertEqual(str(v), s.format("%" + k))

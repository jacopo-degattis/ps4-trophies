from lib.trophy import Trophy

if __name__ == "__main__":
    t = Trophy("./TROPHY.TRP", "NPWR32931_00")

    print(t.header.version)
    print(t.entries[0].name)

    t.extract_files()
    t.decrypt_esfm_file("./NPWR32931_00/TROP.ESFM")

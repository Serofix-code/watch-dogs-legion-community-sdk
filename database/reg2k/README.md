# reg2k catalog cache

Run `python tools/import_reg2k_gists.py --output database/reg2k` to refresh
these normalized, provenance-preserving catalogs. The generated JSON files are
reference data for name/hash lookup only; they do not contain game binaries or
save data and do not establish a safe runtime memory patch.

#%%
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import re
ALPHABET =  ["-", 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y','X', 'B', 'Z', 'J']
ALPHABET = "".join(ALPHABET)

msa_pattern = re.compile(rf">\w+\\n[{ALPHABET}]+")

lines = []

with open("bats.txt", 'r') as f:
    lines = f.read().splitlines()

bat_names = [name.replace(" ", "_") for name in lines]

def parse_msa(msa_file: Path) -> dict[str,str]:
    with ZipFile(msa_file, 'r') as msazip:
        with msazip.open(f"omm_filtered_AA_CDS/{msa_file.stem}", "r") as f:
            msalist = msa_pattern.findall(str(f.read()))
    
    msalist = [x[1:] for x in msalist]
    msa = {}
    # print(msalist)
    for item in msalist:
        temp = item.split("\\n")
        species, seq  = temp[0], temp[1]
        msa[species] = seq
    return msa

def separate_bats_msa_from_others(alignment: dict[str,str]) -> tuple[dict[str,str], dict[str,str]]:
    bats_msa = {}
    all_others_msa = {}
    for species, sequence in alignment.items():
        if species in bat_names:
            bats_msa[species] = alignment[species]
        else:
            all_others_msa[species] = alignment[species]

    return bats_msa, all_others_msa

common_bats = set()


msa_paths = Path("msas/")
#%%

SPECIES_THRESHOLD = 16
UNIQUE_SEQUENCES_IN_MSA = 14
COUNT = 0

collected_msa_paths = []
filtered_msas: dict[str, tuple[dict[str,str], dict[str,str]]] = {}

for msa_path in msa_paths.iterdir():
    try:
        msa = parse_msa(msa_path)
    except BadZipFile:
        print(msa_path, "is bad!")
        continue
        
    bats_msa, other_msa = separate_bats_msa_from_others(msa)
    number_of_bats_in_msa = len(bats_msa)
    if number_of_bats_in_msa >= SPECIES_THRESHOLD:
        continue
    unique_lengths: set[int] = set()
    for seq in bats_msa.values():
        unique_lengths.add(len(seq.replace("-","")))
    if len(unique_lengths) < UNIQUE_SEQUENCES_IN_MSA:
        continue
    filtered_msas[str(msa_path)] = (bats_msa, other_msa)

    collected_msa_paths.append(str(msa_path))
    COUNT += 1
#%%
print(len(collected_msa_paths))
# %%
with open("filtered_file_paths.txt", "w") as f:
    f.write("\n".join(collected_msa_paths))
# %%
def write_sequences_to_path(path: Path, msa: dict[str,str]):
    msa_str = "\n".join([f">{key}\n{val.replace('-','')}" for key,val in msa.items()])
    with open(path, 'w') as f:
        f.write(msa_str)
    

bat_msas_path = Path("bat_msas").resolve()
other_msas_path = Path("other_msas").resolve()

for msa_path in collected_msa_paths:
    file_name = Path(msa_path).stem.split(".")[0]
    Path.mkdir(bat_msas_path / file_name, exist_ok=True)
    bat_msa, other_msa = filtered_msas[msa_path]
    write_sequences_to_path(bat_msas_path / file_name / "msa.fasta",
                       bat_msa)

    Path.mkdir(other_msas_path / file_name, exist_ok=True)
    write_sequences_to_path(other_msas_path / file_name / "msa.fasta",
                       other_msa)

# %%

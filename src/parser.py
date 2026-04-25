'''def parse_logs(file_path):
    parsed = []

    with open(file_path, "r") as f:
        for line in f:
            if "ERR" in line:
                status = "ERROR"
            elif "TIMEOUT" in line:
                status = "TIMEOUT"
            else:
                status = "OK"

            parsed.append({
                "raw": line.strip(),
                "status": status
            })

    return parsed '''
    
    
    
def parse_logs(file_path):
    print("Opening file:", file_path)

    parsed = []

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            print("Total lines read:", len(lines))

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if "ERR" in line:
                    status = "ERROR"
                elif "TIMEOUT" in line:
                    status = "TIMEOUT"
                else:
                    status = "OK"

                parsed.append({
                    "raw": line,
                    "status": status
                })

    except Exception as e:
        print("ERROR while reading file:", e)

    return parsed
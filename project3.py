import json
summary = {
    "total_lines" : 0,
    "INFO" : 0,
    "WARNING" : 0,
    "ERROR" : 0,
    "malformed_line" : 0
}

with open("server.log" , "r") as file : 
    for line in file:
        summary["total_lines"] += 1
        clean_line = line.strip()   
        
        if not clean_line:
            continue
        
        try: 
            parts = clean_line.split(" ")
            log_level = parts[2].upper()
            
            if log_level in summary:
                summary[log_level] += 1
                
            else:
                summary["malformed_line"] += 1
            
        except IndexError : 
            summary["malformed_line"] += 1 
            
            
with open("log_summery.json" , "w") as file:
    json.dump(summary,file,indent=4)
print("Parsing complete! Check log_summary.json.")


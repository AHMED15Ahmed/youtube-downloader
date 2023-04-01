import os
import json
import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
def extract_format_data(format_data):
    extension = format_data["ext"]
    format_name = format_data["format"]
    url = format_data["url"]
    return {
        "extension": extension,
        "format_name": format_name,
        "url": url
    }


def extract_video_data_from_url(url):
    #command = "youtube-dl.exe --get-url 'https://www.youtube.com/watch?v=L8GxAf-Z8Zc' -j"
    #command = f'yt-dpl"{url}" -j '   
    # output = os.popen(f'yt-dlp {url}-j').read()
    # output = os.popen(f'yt-dlp https://www.youtube.com/watch?v=L8GxAf-Z8Zc -j').read()
    output = os.popen(f'yt-dlp {url} -j').read()
    #print(output)
    # the json file to save the output data   
    # Serializing json
    json_object = json.dumps(json.loads(output), indent=4)
 
    # Writing to sample.json
    with open("output.json", "w") as outfile:
        outfile.write(json_object)

    # with open("output.json", "w") as save_file:
    #     json.dump(json.loads(output), save_file)  
    #save_file.close()  
    video_data = json.loads(json_object)
    title = video_data["title"]
    formats = video_data["formats"]
    thumbnail = video_data["thumbnail"]
    print(thumbnail)
    formats = [extract_format_data(format_data) for format_data in formats]
    return {
        "title": title,
        "formats": formats,
        "thumbnail": thumbnail
    }


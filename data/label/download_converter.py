import urllib.request

def download_github_file(url, output_path):
    # Convert GitHub URL to raw URL
    if 'github.com' in url:
        raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
    else:
        print('Invalid GitHub URL.')
        return

    try:
        urllib.request.urlretrieve(raw_url, output_path)
        print(f'File downloaded successfully and saved to {output_path}.')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    download_github_file(
        "https://github.com/wkentaro/labelme/blob/main/examples/instance_segmentation/labelme2voc.py",
        "labelme2voc.py"
    )

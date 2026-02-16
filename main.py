import time
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FilteredEventHandler(FileSystemEventHandler):
    def __init__(self, keywords):
        self.keywords = [k.lower() for k in keywords]

    def _match(self, path):
        if not self.keywords:
            return True
        path_lower = path.lower()
        return any(k in path_lower for k in self.keywords)

    def on_created(self, event):
        if self._match(event.src_path):
            print(f"[CREATE] {event.src_path}")

    def on_deleted(self, event):
        if self._match(event.src_path):
            print(f"[DELETE] {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory and self._match(event.src_path):
            print(f"[MODIFY] {event.src_path}")

    def on_moved(self, event):
        if self._match(event.src_path) or self._match(event.dest_path):
            print(f"[MOVE] {event.src_path} -> {event.dest_path}")

def main():
    parser = argparse.ArgumentParser(description="フォルダ監視ツール")
    parser.add_argument(
        "-p", "--path",
        required=True,
        help="監視するフォルダのパス"
    )
    parser.add_argument(
        "-k", "--keyword",
        action="append",
        default=[],
        help="絞り込みキーワード（複数指定可）"
    )

    args = parser.parse_args()

    handler = FilteredEventHandler(args.keyword)
    observer = Observer()
    observer.schedule(handler, args.path, recursive=True)
    observer.start()

    print("ファイル監視開始")
    print(f"監視フォルダ: {args.path}")
    print(f"キーワード: {args.keyword if args.keyword else 'なし'}")
    print("Ctrl+C で終了")
    print("==========================")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    main()
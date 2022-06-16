import argparse, os, sys, time

class walk:
    """A class for recurrsively searching large files using dfs.
    
    Can find large files.
    Can find files with certain suffix.
    """
    def __init__(self, root, target_count, suffix, output, delete):
        """Constructor"""
        self.root = root
        self.target_count = target_count
        self.suffix = suffix
        self.output = output
        self.delete = delete
        #
        self.top_sizes = []
        
    def validate_item(self, size):
        if len(self.top_sizes) <= self.target_count:
            self.top_sizes.append(size)
            self.top_sizes.sort(reverse = True)
            return True
        elif size >= self.top_sizes[self.target_count - 1]:
            self.top_sizes[self.target_count - 1] = size
            self.top_sizes.sort(reverse = True)
            return True
        else: return False
        
    def dfs(self, path):
        """dfs"""
        # 
        try:
            os.listdir(path)
        except FileNotFoundError:
            print("Please check the path provided.")
            
        #
        found_path = []
        ## base
        if (len(os.listdir(path)) == 0): return found_path
        
        ## recur
        with os.scandir(path) as it:
            for item in it:
                if item.is_file():
                    # validate
                    if item.path.endswith(self.suffix) and self.validate_item(item.stat().st_size):
                        found_path.append((item.path,item.stat().st_size))
                elif item.is_dir():
                    found_path.extend(self.dfs(item.path))
                    
        return found_path
    
    def formating(self):
        #
        out = sorted(self.dfs(self.root), key = lambda x: x[1], reverse = True)
        #
        if self.target_count > len(out):
            print('Currently looking for the top ', self.target_count, " files, however, only ",len(out), " found.")
            
        # write
        list2write = out[:self.target_count]
        with open(self.output + "_" + self.root + ".txt", 'w') as f:
            f.write("Rank     " + "File path     " + "Size    ")
            f.write('\n')
            for i in range(len(list2write)):
                item = list2write[i]
                f.write(str(i+1) + "     " + item[0] +  "     "  + str(item[1]))
                f.write('\n')

        # delete
        if (self.delete.upper() == 'T'):
            if (len(list2write) < self.target_count):
                print("Some (or all) file(s) not found, may have been deleted already.")
            else:
                for item in list2write:
                    print("Trying to delete " + str(len(list2write)) + " files.")
                    print("\n")
                    #
                    print("Trying to delete " + item[0])
                    os.system("rm " + item[0])
                    time.sleep(.5)
        return

#
def main(args):    
    obj = walk(args.root,
               args.top,
               args.suffix,
               args.output,
               args.delete)
    obj.formating()
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--root',
                        help='The root path to start the search.',
                        type=str,
                        default='./')
    parser.add_argument('--top',
                        help='The total number of file to target.',
                        type=int,
                        default=20)
    parser.add_argument('--suffix',
                        help='The suffix need to be targeted, e.g., .fq will only find files end with .fq',
                        type=str,
                        default='')
    parser.add_argument('--output',
                        help='The path of the output file.',
                        type=str,
                        default='LargeFiles')
    parser.add_argument('--delete',
                        help='If need to delete the files directly.',
                        type=str,
                        default='F')
    args = parser.parse_args()
    main(args)
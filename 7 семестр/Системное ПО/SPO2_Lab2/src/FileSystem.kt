import java.util.HashMap
import java.util.ArrayList
import java.io.Serializable

const val MAX_BLOCK_COUNT = 200
const val MAX_DESCRIPTOR_COUNT = 10
const val BLOCK_SIZE = 8
const val MAX_LINK_COUNT = 10
const val EMPTY_CHAR = '`'
const val sep = '/'
val charset = Charsets.UTF_8

typealias DescriptorIndex = Int
typealias BlockIndex = Int

class FileSystem : Serializable {
    private val root: DescriptorIndex = 0
    var path = mutableListOf("")
    private var currentDirectory: DescriptorIndex = root
    private val dataBlocks = ArrayList(List(MAX_BLOCK_COUNT){DataBlock()})
    private val usedBlocks =  ArrayList(List(MAX_BLOCK_COUNT){false})
    private val descriptors = ArrayList<Descriptor>(List(MAX_DESCRIPTOR_COUNT){Descriptor()})
    private val openedDescriptors = HashMap<Int, DescriptorIndex>()

    init {
        val rootFd = Descriptor(true, 1)
        descriptors[root] = rootFd
        addLinkAtDirectory(rootFd, "..", root)
        addLinkAtDirectory(rootFd, ".", root)
    }

    fun fileStat(fdIdx: DescriptorIndex) {
        if (fdIdx in 0..(MAX_DESCRIPTOR_COUNT - 1)) {
            val fd = descriptors[fdIdx]
            println("RefCount = ${fd.refCount}, size = ${fd.size}, links to file blocks: ${fd.linksToBlocks}")
        } else {
            println("There is no descriptor with id $fdIdx")
        }
    }

    fun createFile(fileName: String): DescriptorIndex? {
        val fdIdx = getEmptyDescriptor()
        if (fdIdx == null) {
            println("There are no empty descriptors, file creation failed")
            return null
        }
        val fd = Descriptor(false, 1)
        descriptors[fdIdx] = fd

        val parentDir = descrPathLookup(fileName) ?: return null
        addLinkAtDirectory(descriptors[parentDir], getFileNameFromPath(fileName), fdIdx)
        return fdIdx
    }

    fun openFile(fileName: String){
        val fd = descrLookup(fileName) ?: return
        val fdId = getFdId()
        openedDescriptors[fdId] = fd
        println("File [${getFileNameFromPath(fileName)}] was opened FD = $fdId")
    }

    fun closeFile(fdId: Int){
        openedDescriptors.remove(fdId)
        println("Completed")
    }

    fun ls() {
        val currentDir = descriptors[currentDirectory]
        val files = HashMap<String, Int>()
        val dirs = HashMap<String, Int>()
        for (i in 0 until currentDir.linksToBlocks.size step 2) {
            val nameBlock = dataBlocks[currentDir.linksToBlocks[i]]
            val linkBlock = dataBlocks[currentDir.linksToBlocks[i+1]]
            val name = getFileName(nameBlock)
            val fdIdx = getFdIdx(linkBlock)
            val fd = descriptors[fdIdx]
            if (fd.isFolder) {
                dirs[name] = fdIdx
            } else {
                files[name] = fdIdx
            }
        }
        println("Directories:")
        for (dir in dirs) {
            println("\t$dir")
        }
        println("Files:")
        for (file in files) {
            println("\t$file")
        }
    }

    fun readFile(fdId: Int, offset: Int, size: Int) {
        val fdIdx = openedDescriptors[fdId]
        if (fdIdx == null) {
            println("There isn't opened file with FD = $fdId")
            return
        }
        val fd = descriptors[fdIdx]
        var data = ""
        for (blockIdx in fd.linksToBlocks) {
            data += dataBlocks[blockIdx].data.toString(charset)
        }
        data = data.substring(offset, offset + size)
        println("Result: \n $data")
    }

    fun writeToFile(fdId: Int, offset: Int, size: Int, inputData: String){
        var data = inputData
        if (data.length > size)
            data = data.substring(0, size)

        val fdIdx = openedDescriptors[fdId]
        if (fdIdx == null) {
            println("There isn't opened file with FD = $fdId")
            return
        }
        val fd = descriptors[fdIdx]

        val startBlock = offset / BLOCK_SIZE
        var endBlock = (offset + size) / BLOCK_SIZE
        if (endBlock > MAX_BLOCK_COUNT)
            endBlock = MAX_BLOCK_COUNT - 1

        while (fd.linksToBlocks.count() < endBlock + 1) {
            val blockIdx = getFirstFreeBlock() ?: return
            fd.addLinkToBlock(blockIdx)
        }

        val startIdx = offset % BLOCK_SIZE

        if (startBlock == endBlock) {
            val block = dataBlocks[fd.linksToBlocks[startBlock]]
            block.writeData(data, startIdx)
        } else {
            for (i in startBlock..endBlock) {
                val block = dataBlocks[fd.linksToBlocks[i]]
                when (i) {
                    startBlock -> {
                        block.writeData(data.substring(0 until BLOCK_SIZE - startIdx), startIdx)
                        data = data.drop(BLOCK_SIZE - startIdx)
                    }
                    endBlock -> block.writeData(data, 0)
                    else -> {
                        block.writeData(data)
                        data = data.drop(BLOCK_SIZE)
                    }
                }
            }
        }
        println("Completed")
    }

    fun link(fileName: String, linkName: String){
        val fd = descrLookup(fileName) ?: return
        descriptors[fd].refCount += 1

        val parentDir = descrPathLookup(fileName) ?: return
        addLinkAtDirectory(descriptors[parentDir], linkName, fd)

        println("${getFileNameFromPath(fileName)} linked to $linkName")
    }
    
    fun unlink(linkName: String) {
        val fdIdx = descrLookup(linkName) ?: return
        val parentDirIdx = descrPathLookup(linkName) ?: return
        val parentDir = descriptors[parentDirIdx]
        val fd = descriptors[fdIdx]
        fd.refCount -= 1
        for (i in 0 until parentDir.linksToBlocks.size step 2) {
            val nameBlock = dataBlocks[parentDir.linksToBlocks[i]]
            if (getFileName(nameBlock) == linkName) {
                parentDir.linksToBlocks.removeAt(i)
                parentDir.linksToBlocks.removeAt(i)
                break
            }
        }

        if ( fd.refCount == 0) {
            for (i in 0 until fd.size) {
                val blockIdx = fd.linksToBlocks[i]
                dataBlocks[blockIdx].fillWithBlanks(0 until BLOCK_SIZE)
                usedBlocks[blockIdx] = false
            }
            descriptors[fdIdx] = Descriptor()
        }

        println("Completed")
    }
    
    fun truncate(fileName: String, size: Int){
        val fdIdx = descrLookup(fileName) ?: return
        val fd = descriptors[fdIdx]

        val endBlockInFd = size / BLOCK_SIZE
        val fileBlocksCount = fd.size
        if (endBlockInFd + 1 > fileBlocksCount) {
            for (i in fileBlocksCount..endBlockInFd) {
                val blockIdx = getFirstFreeBlock() ?: return
                val block = dataBlocks[blockIdx]
                block.fillWithBlanks(0 until BLOCK_SIZE)
            }
        } else {
            val endBlock = dataBlocks[fd.linksToBlocks[endBlockInFd]]
            val bytesUnEndBlock = size % BLOCK_SIZE
            endBlock.fillWithBlanks(bytesUnEndBlock until BLOCK_SIZE)
            //endBlock.data = endBlock.data.take(bytesUnEndBlock) + " ".repeat(BLOCK_SIZE - bytesUnEndBlock)
            for (i in endBlockInFd + 1 until fileBlocksCount) {
                val blockIdx = fd.linksToBlocks[i]
                usedBlocks[blockIdx] = false
                val block = dataBlocks[blockIdx]
                block.fillWithBlanks(0 until BLOCK_SIZE)
            }
        }
        println("Completed")
    }

    fun mkdir(dirName: String) {
        val fdIdx = getEmptyDescriptor()
        if (fdIdx == null) {
            println("There are no empty descriptors, directory creation failed")
            return
        }
        val fd = Descriptor(true, 1)
        descriptors[fdIdx] = fd

        val parentDir = descrPathLookup(dirName) ?: return
        addLinkAtDirectory(descriptors[parentDir], getFileNameFromPath(dirName), fdIdx)
        createDirectoryLinks(parentDir, fdIdx)

        println("Directory created.")
    }

    fun rmdir(dirName: String) {
        val fdIdx = descrLookup(dirName) ?: return
        val parentDirIdx = descrPathLookup(dirName) ?: return
        val fd = descriptors[fdIdx]
        val parentDir = descriptors[parentDirIdx]

        for (i in 0 until fd.linksToBlocks.size step 2) {
            val nameBlock = dataBlocks[fd.linksToBlocks[i]]
            val name = getFileName(nameBlock)
            if (name != "." && name != "..") {
                println("Directory is not empty, deletion failed.")
                return
            }
        }

        val nameWithoutPath = getFileNameFromPath(dirName)
        for (i in 0 until parentDir.linksToBlocks.size step 2) {
            val nameBlock = dataBlocks[parentDir.linksToBlocks[i]]
            if (getFileName(nameBlock) == nameWithoutPath) {
                parentDir.linksToBlocks.removeAt(i)
                parentDir.linksToBlocks.removeAt(i)
                break
            }
        }

        descriptors[fdIdx] = Descriptor()

        println("Completed")
    }

    fun cd(dirName: String) {
        val fdIdx = descrLookup(dirName, currentDirectory, true) ?: return
        currentDirectory = fdIdx
    }

    fun cd() {
        currentDirectory = root
        path = mutableListOf("")
    }

    fun symlink(pathName: String, linkName: String) {
        val fdIdx = createFile(linkName) ?: return
        val steps = pathName.split(sep)
        if (steps.count() > MAX_LINK_COUNT / 2){
            println("Path is too long, symlink creation failed.")
            return
        }
        val fd = descriptors[fdIdx]
        for (step in steps) {
            val blockIdx = getFirstFreeBlock() ?: return
            fd.addLinkToBlock(blockIdx)
            if (step.length > BLOCK_SIZE) {
                println("Name $step is too long, symlink creation failed.")
                return
            }
            val block = dataBlocks[blockIdx]
            block.writeData(step)
        }
    }

    private fun createDirectoryLinks(parentIdx: DescriptorIndex, fdIdx: DescriptorIndex) {
        val fd = descriptors[fdIdx]
        addLinkAtDirectory(fd, "..", parentIdx)
        addLinkAtDirectory(fd, ".", fdIdx)
    }

    private fun getEmptyDescriptor(): DescriptorIndex? {
        val fdIdx = descriptors.indexOfFirst { it.refCount == 0 }
        return if (fdIdx == -1) null else fdIdx
    }

    private fun getFirstFreeBlock(): BlockIndex? {
        val blockIdx = usedBlocks.indexOfFirst { !it }
        return if (blockIdx == -1) {
            println("There are no free blocks, operation failed.")
            null
        } else  {
            usedBlocks[blockIdx] = true
            blockIdx
        }
    }

    private fun getFdId(): Int {return if (openedDescriptors.isEmpty()) 0 else (openedDescriptors.keys.max()!! + 1)}

    private fun addLinkAtDirectory(directory: Descriptor, fileName: String, fdIdx: DescriptorIndex) {
        if (!directory.isFolder) return
        val nameBlock = getFirstFreeBlock() ?: return
        val linkBlock = getFirstFreeBlock() ?: return
        directory.addLinkToBlock(nameBlock)
        directory.addLinkToBlock(linkBlock)
        dataBlocks[nameBlock].writeData(fileName)
        dataBlocks[linkBlock].data[0] = fdIdx.toByte()
    }

    private fun getFileName(block: DataBlock): String {return block.data.toString(charset).trim(EMPTY_CHAR) }

    private fun getFdIdx(block: DataBlock): Int {return block.data[0].toInt()}

    private fun descrPathLookup(filename: String): DescriptorIndex? {
        // returns descriptor of direct parent of file
        val lastSep = filename.lastIndexOf(sep)
        if (lastSep == -1) {
            return currentDirectory
        }
        return descrLookup(filename.substring(0 until lastSep))
    }

    private fun descrLookup(name: String, currentDirIdx: DescriptorIndex = currentDirectory, updatePath: Boolean = false): DescriptorIndex? {
        // returns descriptor of file
        val steps = name.split(sep)
        var fdIdx: DescriptorIndex = currentDirIdx
        for (step in steps) {
            var success = false
            val currentDir = descriptors[fdIdx]
            for (i in 0 until currentDir.linksToBlocks.size step 2) {
                val nameBlock = dataBlocks[currentDir.linksToBlocks[i]]
                if (getFileName(nameBlock) == step) {
                    val linkBlock = dataBlocks[currentDir.linksToBlocks[i+1]]
                    val parentIdx = fdIdx
                    fdIdx = getFdIdx(linkBlock)
                    val fd = descriptors[fdIdx]
                    if (!fd.isFolder) {
                        val pathFromLink = getPathFromSymLink(fd)
                        val idx = descrLookup(pathFromLink, parentIdx, updatePath)
                        if (idx == null) {
                            println("$step is not valid link, failed.")
                        } else {
                            fdIdx = idx
                        }
                    } else if (updatePath) {
                        if (step == "..") {
                            path = path.dropLast(1).toMutableList()
                        } else {
                            path.add(step)
                        }
                    }
                    success = true
                }
            }
            if (!success) {
                println("$step is not a directory or valid symlink.")
                return null
            }
        }
        return fdIdx
    }

    private fun getPathFromSymLink(file: Descriptor): String {
        val result = mutableListOf<String>()
        for (i in 0 until file.size) {
            val step = getFileName(dataBlocks[file.linksToBlocks[i]])
            result.add(step)
        }
        return result.joinToString(sep.toString())
    }

    private fun getFileNameFromPath(path: String): String {return path.split(sep).last()}
}
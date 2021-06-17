import java.io.ObjectOutputStream
import java.io.FileOutputStream
import java.io.File
import java.io.ObjectInputStream
import java.io.FileInputStream
import java.io.IOException
import java.util.*

const val WRONG_ARG_NUMBER_EXCEPTION = "Wrong number of arguments."
const val NO_SYSTEM_EXCEPTION = "File system was not mounted."
const val EXT = ".fs"

object Main {
    var scan = Scanner(System.`in`)
    var fileSystem: FileSystem? = null

    fun mount(args: List<String>) {
        when (args.count()) {
            0 -> {
                fileSystem = FileSystem()
                println("Mounted empty file system.")
            }
            1 -> {
                val fileName = args[0]
                if (!fileName.contains(EXT)) {
                    println("Wrong type of file, mount failed.")
                    return
                }
                val file = File(fileName)
                if (file.exists()) {
                    val fileIn: FileInputStream
                    try {
                        fileIn = FileInputStream(file.absolutePath)
                        val in1 = ObjectInputStream(fileIn)
                        fileSystem = in1.readObject() as FileSystem
                        in1.close()
                        fileIn.close()
                    } catch (e: Exception) {
                        println("Mount failed.")
                        e.printStackTrace()
                    }
                    println("Mounted file system from file $fileName.")
                } else {
                    println("File $fileName doesn't exist")
                }
            }
            else -> { println(WRONG_ARG_NUMBER_EXCEPTION) }
        }
    }

    fun unmount(args: List<String>) {
        if (checkArgsCount(args, 1)) {
            val fileName = args[0]
            val myFile = File(fileName)
            val fileOut: FileOutputStream
            try {
                fileOut = FileOutputStream(myFile.path + if (fileName.contains(EXT)) "" else EXT)
                val out = ObjectOutputStream(fileOut)
                out.writeObject(fileSystem)
                out.close()
                fileOut.close()
                println("Unmounted file system to file $fileName.")
            } catch (e: Exception) {
                println("Unmount failed.")
                e.printStackTrace()
            }
        }
    }

    fun filestat(args: List<String>) {
        if (checkArgsCount(args, 1)) {
            val id = Integer.parseInt(args[0])
            fileSystem?.fileStat(id) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun create(args: List<String>) {
        if (checkArgsCount(args, 1)) {
            val fileName = args[0]
            fileSystem?.createFile(fileName) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun ls(args: List<String>) {
        if (checkArgsCount(args, 0)){
            fileSystem?.ls() ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun open(args: List<String>) {
        if (checkArgsCount(args, 1)) {
            val fileName = args[0]
            fileSystem?.openFile(fileName) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun close(args: List<String>) {
        if (checkArgsCount(args, 1)) {
            val fdIdx = Integer.parseInt(args[0])
            fileSystem?.closeFile(fdIdx) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun read(args: List<String>) {
        if (checkArgsCount(args, 3)) {
            val fdIdx = Integer.parseInt(args[0])
            val offset = Integer.parseInt(args[1])
            val size = Integer.parseInt(args[2])
            fileSystem?.readFile(fdIdx, offset, size) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun write(args: List<String>) {
        if (checkArgsCount(args, 4)) {
            val fdIdx = Integer.parseInt(args[0])
            val offset = Integer.parseInt(args[1])
            val size = Integer.parseInt(args[2])
            val inputData = args[3]
            fileSystem?.writeToFile(fdIdx, offset, size, inputData) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun link(args: List<String>) {
        if (checkArgsCount(args, 2)) {
            val fileName = args[0]
            val linkName = args[1]
            fileSystem?.link(fileName, linkName) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun unlink(args: List<String>) {
        if (checkArgsCount(args, 1)) {
            val linkName = args[0]
            fileSystem?.unlink(linkName) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun truncate(args: List<String>) {
        if (checkArgsCount(args, 2)) {
            val fileName = args[0]
            val size = Integer.parseInt(args[1])
            fileSystem?.truncate(fileName, size) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun mkdir(args: List<String>) {
        if (checkArgsCount(args, 1)) {
            val dirName = args[0]
            fileSystem?.mkdir(dirName) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun rmdir(args: List<String>) {
        if (checkArgsCount(args, 1)) {
            val dirName = args[0]
            fileSystem?.rmdir(dirName) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    fun cd(args: List<String>) {
        if (args.count() == 1) {
            val dirName = args[0]
            fileSystem?.cd(dirName) ?: println("NO_SYSTEM_EXCEPTION")
        } else if (args.isEmpty()) {
            fileSystem?.cd() ?: println("NO_SYSTEM_EXCEPTION")
        } else {
            println(WRONG_ARG_NUMBER_EXCEPTION)
        }
    }

    fun symlink(args: List<String>) {
        if (checkArgsCount(args, 2)) {
            val pathName = args[0]
            val linkName = args[1]
            fileSystem?.symlink(pathName, linkName) ?: println("NO_SYSTEM_EXCEPTION")
        }
    }

    @JvmStatic
    fun main(globalArgs: Array<String>) {
        while (true) {
            if (fileSystem != null) {
                val path = fileSystem!!.path.joinToString(sep.toString())
                print("$path> ")
            }
            val input = readLine() ?: ""
            val (command, args) = getCommandAndArgs(input)
            var exit = false
            try {
                when (command) {
                    "mount" -> mount(args)
                    "unmount" -> unmount(args)
                    "filestat" -> filestat(args)
                    "create" -> create(args)
                    "ls" -> ls(args)
                    "open" -> open(args)
                    "close" -> close(args)
                    "read" -> read(args)
                    "write" -> write(args)
                    "link" -> link(args)
                    "unlink" -> unlink(args)
                    "truncate" -> truncate(args)
                    "mkdir" -> mkdir(args)
                    "rmdir" -> rmdir(args)
                    "cd" -> cd(args)
                    "symlink" -> symlink(args)
                    "exit" -> {exit = true}
                    "q" -> {exit = true}
                    else -> {println("Unknown command")
                    }
                }
            } catch (e: IOException) {
                e.printStackTrace()
            }
            if (exit)
                break
        }
    }

    private fun checkArgsCount(args: List<String>, n: Int): Boolean {
        if (args.count() != n) {
            println(WRONG_ARG_NUMBER_EXCEPTION)
            return false
        }
        return true
    }

    private fun getCommandAndArgs(input: String): Pair<String, List<String>> {
        val args = input.split(" ").toMutableList()
        val command = args.removeAt(0)
        return command to args
    }
}
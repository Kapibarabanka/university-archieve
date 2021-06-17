import java.util.ArrayList
import java.io.Serializable

class Descriptor(
    var isFolder: Boolean,
    var refCount: Int) : Serializable {
    constructor(): this(false, 0)

    val size: Int
        get() {return linksToBlocks.count()}

    val linksToBlocks = ArrayList<BlockIndex>()

    fun addLinkToBlock(blockIndex: BlockIndex) {
        if (linksToBlocks.count() < MAX_LINK_COUNT)
            linksToBlocks.add(blockIndex)
        else
            println("Cannot add new link to this file")
    }
}
// 把 PDF 每一页渲染成 PNG，检查导出效果用：swift tools/pdf_pages.swift portfolio.pdf 输出目录
import AppKit
import PDFKit

let args = CommandLine.arguments
guard args.count == 3, let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    print("用法：swift tools/pdf_pages.swift <pdf> <输出目录>")
    exit(1)
}
let outDir = URL(fileURLWithPath: args[2])
try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
for i in 0..<doc.pageCount {
    guard let page = doc.page(at: i) else { continue }
    let box = page.bounds(for: .mediaBox)
    let scale: CGFloat = 1.4
    let image = page.thumbnail(of: NSSize(width: box.width * scale, height: box.height * scale), for: .mediaBox)
    guard let tiff = image.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff),
          let png = rep.representation(using: .png, properties: [:]) else { continue }
    try png.write(to: outDir.appendingPathComponent(String(format: "page-%02d.png", i + 1)))
}
print("\(doc.pageCount) 页")

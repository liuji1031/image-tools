class: CommandLineTool
cwlVersion: v1.2

inputs:
  inputPath:
    inputBinding:
      prefix: --inputPath
    type: Directory
  filePattern:
    inputBinding:
      prefix: --filePattern
    type: string?
  outputPath:
    inputBinding:
      prefix: --outputPath
    type: Directory
  outImgName:
    inputBinding:
      prefix: --outImageName
    type: string?
  minDim:
    inputBinding:
      prefix: --minDim
    type: int
  outputFormat:
    inputBinding:
      prefix: --outputFormat
    type: string
  downsampleMethod:
    inputBinding:
      prefix: --downsampleMethod
    type: string?

outputs:
  outputPath:
    outputBinding:
      glob: $(inputs.outputPath.basename)
    type: Directory

requirements:
  DockerRequirement:
    dockerPull: polusai/pyramid-generator-2d-tool:0.1.1-dev0
  InitialWorkDirRequirement:
    listing:
    - entry: $(inputs.outDir)
      writable: true
  InlineJavascriptRequirement: {}

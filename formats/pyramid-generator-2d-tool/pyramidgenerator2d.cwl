class: CommandLineTool
cwlVersion: v1.2

inputs:
  inpDir:
    inputBinding:
      prefix: --inpDir
    type: Directory
  filePattern:
    inputBinding:
      prefix: --filePattern
    type: string?
  outDir:
    inputBinding:
      prefix: --outDir
    type: Directory
  outImgName:
    inputBinding:
      prefix: --outImageName
    type: string?
  minDim:
    inputBinding:
      prefix: --minDim
    type: int
  outFormat:
    inputBinding:
      prefix: --outFormat
    type: string
  dsMethod:
    inputBinding:
      prefix: --dsMethod
    type: string?

outputs:
  outDir:
    outputBinding:
      glob: $(inputs.outDir.basename)
    type: Directory

requirements:
  DockerRequirement:
    dockerPull: polusai/pyramid-generator-2d-tool:0.1.1-dev0
  InitialWorkDirRequirement:
    listing:
    - entry: $(inputs.outDir)
      writable: true
  InlineJavascriptRequirement: {}

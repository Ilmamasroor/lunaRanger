import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { brotliDecompressSync } from 'node:zlib';

const buildFiles = ['LunaRangers.loader.js', 'LunaRangers.data', 'LunaRangers.framework.js', 'LunaRangers.wasm'];

export async function stageUnity(exportDirectory, destination = 'public/Build') {
  const files = await Promise.all(buildFiles.map(async name => {
    const path = join(exportDirectory, 'Build', name);
    try {
      return await readFile(path);
    } catch (error) {
      if (error.code !== 'ENOENT' || name.endsWith('.loader.js')) throw error;
      return brotliDecompressSync(await readFile(path + '.br'));
    }
  }));
  await mkdir(destination, { recursive: true });
  await Promise.all(buildFiles.map((name, index) => writeFile(join(destination, name), files[index])));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (!process.argv[2]) throw new Error('Usage: node scripts/stage-unity.mjs <Unity export directory>');
  await stageUnity(process.argv[2]);
}

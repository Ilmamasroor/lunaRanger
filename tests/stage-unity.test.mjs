import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { brotliCompressSync } from 'node:zlib';
import { stageUnity } from '../scripts/stage-unity.mjs';

test('stages Unity payloads as decoded files with the names React loads', async () => {
  const root = await mkdtemp(join(tmpdir(), 'lunarangers-stage-'));
  try {
    const source = join(root, 'source');
    const target = join(root, 'target');
    await mkdir(join(source, 'Build'), { recursive: true });
    const files = {
      'LunaRangers.loader.js': Buffer.from('loader'),
      'LunaRangers.data': Buffer.from('data'),
      'LunaRangers.framework.js': Buffer.from('framework'),
      'LunaRangers.wasm': Buffer.from([0, 97, 115, 109]),
    };
    for (const [name, bytes] of Object.entries(files)) {
      const loader = name.endsWith('loader.js');
      await writeFile(join(source, 'Build', loader ? name : name + '.br'), loader ? bytes : brotliCompressSync(bytes));
    }
    await stageUnity(source, target);
    for (const [name, bytes] of Object.entries(files)) {
      assert.deepEqual(await readFile(join(target, name)), bytes);
    }
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

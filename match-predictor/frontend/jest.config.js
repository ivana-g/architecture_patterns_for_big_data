/** @type {import('ts-jest/dist/types').InitialOptionsTsJest} */
export default {
    preset: 'ts-jest',
    testEnvironment: 'jsdom',
    moduleNameMapper: {
        '\\.[cC][sS][sS]$': '<rootDir>/src/TestSupport/AssetStubs.js',
        '\\.[sS][vV][gG]$': '<rootDir>/src/TestSupport/AssetStubs.js',
    },
    globals: {'ts-jest': {useESM: true, isolatedModules: true}},
    setupFilesAfterEnv: ['<rootDir>/src/TestSupport/GlobalHelpers.js']
};
